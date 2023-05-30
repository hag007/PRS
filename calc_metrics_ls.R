# .libPaths(c('../R-env/prs-R',.libPaths()))
source('constants.R')
source('utils.R')
source('calc_metrics_generic.R')

method="ls"
grid.ids.default <- c(0.2,0.5,0.9,1)
args <- commandArgs(trailing = TRUE)
parse.args(args, grid.ids.default, method)

grid.ids.full=c()
for(a in grid.ids){
    for(b in seq(1,20)){
        grid.ids.full <- append(grid.ids.full, paste0(a,"-",b))
    }
}

calc.metrics(target.path, imp.name, prs.rep.path, sub, grid.ids.full, prs.prefix, cv.test.suffix, rep)


