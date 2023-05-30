.libPaths(c('../R-env/prs-R',.libPaths()))
source('constants.R')
source('utils.R')
source('calc_metrics_generic.R')

method="cs"
grid.ids.default <- c(0)
args <- commandArgs(trailing = TRUE)
parse.args(args, grid.ids.default, method)

calc.metrics(target.path, imp.name, prs.rep.path, sub, grid.ids, prs.prefix, cv.test.suffix, rep, prs.prefix)
