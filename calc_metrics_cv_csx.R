# .libPaths(c('../R-env/prs-R',.libPaths()))
source('constants.R')
source('utils.R')
source('calc_metrics_generic.R')

method="csx"
a.default <- c(0.5,1,1.5,1)
b.default <- c(0.5,0.5,0.5,1)
grid.ids.full <- c()
analysis.type <- "cv"

for (i in seq_len(length(a.default))){
	a <- a.default[i]
	b <- b.default[i]
	grid.ids.full <- paste(grid.ids.full, paste0(a,"-",b), sep= ",")
}
grid.ids.full<- substring(grid.ids.full, 2)

args <- commandArgs(trailing = TRUE)
parse.args(args, grid.ids.full, method)

calc.metrics(target.path, imp, prs.path, sub, grid.ids, prs.prefix, suffix, rep, analysis.type)
