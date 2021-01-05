.libPaths('/specific/elkon/hagailevi/PRS/prs-R')

library(proxysnps)
d <- get_proxies(query = "rs42")
plot(d$POS, d$R.squared, main="rs42", xlab="Position", ylab=bquote("R"^2))

