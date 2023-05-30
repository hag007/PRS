library('WebPower')
library('powerMediation')

n=8000

cases=c(3075,914,1013,800,508,410,176,256,255,206,243,487,237,2968,1924,1229,1547,559,529,611,402,439,549,291,119,360)



for(i in cases){

    # wp.logistic(n = n, p0 = 1/2, p1 = (1+0.01*seq(0,50)) / (2+0.01*seq(0,50)), family='normal', alpha = 0.05)['power']
    y <-  powerLogisticCon(n=n,p=i/n, OR=1+seq(1:50)/100 )
    for(j in 1:length(y)){
        if(y[j] >0.8){
            print(paste(i,1+seq(1:50)[j]/100))
            break
        }
    }    
        
    # plot(1+seq(1:50)/100, y)
    # png(file=paste0("test_",i,".png"), width=600, height=350)

}
