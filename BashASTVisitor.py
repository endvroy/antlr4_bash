from gen.BashParserVisitor import BashParserVisitor
from gen.BashParser import BashParser
from bash_ast import BashAST

# in decreasing order
REDIR_ORDER = ['LT',
               'GT',
               'LT_AND',
               'GT_AND',
               'AND_GT',
               'AND_DGT',
               'DLT',
               'TLT',
               'DLT_DASH',
               'DGT',
               'LTGT',
               'GTPIPE']


class BashASTVisitor(BashParserVisitor):
    def visitPipeline(self, ctx: BashParser.PipelineContext):
        if ctx is None:
            return None
        ast = BashAST(kind='pipeline')
        ast.prev = self.visitPipeline(ctx.pipeline())
        ast.last_cmd = self.visitCmd(ctx.cmd())
        return ast

    def visitCmd(self, ctx: BashParser.CmdContext):
        if ctx is None:
            return None
        ast = BashAST(kind='cmd')
        prefix = self.visitExec_prefix(ctx.exec_prefix())
        prog, suffix = self.visitExec(ctx.exec())
        ast.prog = prog

        # reorganize prefix and suffix
        assign_list = []
        args = []
        redir_list = []
        for node in prefix:
            if node.kind == 'assign':
                assign_list.append(node)
            else:
                redir_list.append(node)
        for node in suffix:
            if node.kind == 'arg':
                args.append(node)
            else:
                redir_list.append(node)
        # todo: reorganize prefix and suffix here
        ast.assign_list = assign_list
        ast.args = args
        ast.redir = redir_list
        return ast

    def visitExec(self, ctx: BashParser.ExecContext):
        if ctx is None:
            return [], []
        prog = self.visitProg(ctx.prog())
        suffix = self.visitExec_suffix(ctx.exec_suffix())
        # if ctx.redir():
        #     imm_redir = self.visitRedir(ctx.redir())
        #     suffix.append(imm_redir)
        return prog, suffix

    def visitExec_prefix(self, ctx: BashParser.Exec_prefixContext):
        if ctx is None:
            return []
        prev_parts = self.visitExec_prefix(ctx.exec_prefix())
        if ctx.redir():
            part_ast = self.visitRedir(ctx.redir())
        elif ctx.assign():
            part_ast = self.visitAssign(ctx.assign())
        else:
            raise ValueError('unrecognized prefix {}'.format(ctx))
        prev_parts.append(part_ast)
        return prev_parts

    def visitExec_suffix(self, ctx: BashParser.Exec_suffixContext):
        if ctx is None:
            return []
        prev_parts = self.visitExec_suffix(ctx.exec_suffix())
        if ctx.redir():
            part_ast = self.visitRedir(ctx.redir())
        elif ctx.arg():
            part_ast = self.visitArg(ctx.arg())
        else:
            raise ValueError('unrecognized suffix {}'.format(ctx))
        prev_parts.append(part_ast)
        return prev_parts

    def visitAssign(self, ctx: BashParser.AssignContext):
        lhs = ctx.VARNAME().getText()
        rhs = self.visitAssign_rls(ctx.assign_rls())
        ast = BashAST(kind='assign', lhs=lhs, rhs=rhs)
        return ast

    def visitAssign_rls(self, ctx: BashParser.Assign_rlsContext):
        parts = self.gather_parts(ctx)
        ast = BashAST(kind='assign_rhs', parts=parts)
        return ast

    def visitRedir(self, ctx: BashParser.RedirContext):
        if ctx.NUM():
            lhs = ctx.NUM().getText()
        else:
            lhs = None

        redir_type = self.visitRedir_op(ctx.redir_op())

        rhs = self.visitArg(ctx.arg())

        redir_ast = BashAST(kind='redir',
                            type=redir_type,
                            lhs=lhs,
                            rhs=rhs)

        return redir_ast

    def visitRedir_op(self, ctx: BashParser.Redir_opContext):
        assert ctx.getChildCount() == 1

        redir_op_sym_idx = ctx.children[0].getSymbol().type
        redir_type = BashParser.symbolicNames[redir_op_sym_idx]
        return redir_type

    def gather_parts(self, ctx):
        parts = []
        if ctx.getChildCount():
            for child in ctx.children:
                try:
                    # leaf node
                    sym_idx = child.getSymbol().type
                    sym_name = BashParser.symbolicNames[sym_idx]
                    lexeme = child.getText()
                    part_ast = BashAST(kind=sym_name, value=lexeme)
                except AttributeError:
                    # todo: delegate
                    part_ast = self.visit(child)
                parts.append(part_ast)
        return parts

    def visitProg(self, ctx: BashParser.ProgContext):
        prog_parts = self.gather_parts(ctx)
        prog_ast = BashAST(kind='prog', parts=prog_parts)
        return prog_ast

    def visitArg(self, ctx: BashParser.ArgContext):
        arg_parts = self.gather_parts(ctx)
        arg_ast = BashAST(kind='arg', parts=arg_parts)
        return arg_ast

    def visitSubst(self, ctx: BashParser.SubstContext):
        assert ctx.getChildCount() == 1
        return self.visit(ctx.children[0])

    def visitCst(self, ctx: BashParser.CstContext):
        pipeline = self.visitPipeline(ctx.pipeline())
        return BashAST(kind='cst', pipeline=pipeline)

    def visitLpst(self, ctx: BashParser.LpstContext):
        pipeline = self.visitPipeline(ctx.pipeline())
        return BashAST(kind='lpst', pipeline=pipeline)

    def visitRpst(self, ctx: BashParser.RpstContext):
        pipeline = self.visitPipeline(ctx.pipeline())
        return BashAST(kind='rpst', pipeline=pipeline)

    def visitArith(self, ctx: BashParser.ArithContext):
        pipeline = self.visitPipeline(ctx.pipeline())
        return BashAST(kind='arith_subst', pipeline=pipeline)

    def visitParam_exp(self, ctx: BashParser.Param_expContext):
        var = ctx.VARNAME().getText()
        if ctx.HASH():
            ast = BashAST(kind='param_exp_hash', var=var)
        else:
            op = self.visitParam_exp_op(ctx.param_exp_op())
            rhs = self.visitAssign_rls(ctx.assign_rls())
            ast = BashAST(kind='param_exp_repl',
                          var=var,
                          op=op,
                          rhs=rhs)
        # todo: more cases may be added for param exp later
        return ast

    def visitParam_exp_op(self, ctx: BashParser.Param_exp_opContext):
        return [x.getText() for x in ctx.children]

    def visitDquote_str(self, ctx: BashParser.Dquote_strContext):
        dquote_parts = self.gather_parts(ctx)
        ast = BashAST(kind='dquote_str', parts=dquote_parts[1:-1])  # filter out dquotes
        return ast

    def visitGrp(self, ctx: BashParser.GrpContext):
        assert ctx.getChildCount() == 1
        return self.visit(ctx.children[0])

    def visitParen_grp(self, ctx: BashParser.Paren_grpContext):
        pipeline = self.visitPipeline(ctx.pipeline())
        ast = BashAST(kind='paren_grp', pipeline=pipeline)
        return ast

    def visitCurly_grp(self, ctx: BashParser.Curly_grpContext):
        pipeline = self.visitPipeline(ctx.pipeline())
        ast = BashAST(kind='curly_grp', pipeline=pipeline)
        return ast

    def visitPure_curly(self, ctx: BashParser.Pure_curlyContext):
        if ctx.LCURLY():
            value = '{'
        else:
            value = '}'
        return BashAST(kind='NAME', value=value)
