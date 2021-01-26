library(httr)
library(jsonlite)
library(xml2)
library(hash)

source.rsids <- scan("source_rsid.txt", what=character(), sep="\n")
available.rsids <- as.character(scan("dest_rsid.txt", what=character(), sep="\n"))
mapped.rsids <- hash() 

for(s_r in source.rsids){

if(s_r %in% available.rsids)
{
	mapped.rsids[[s_r]] <- s_r
        print("source rsid is available")
	print(paste0(s_r,"->",s_r))
        next    
}


server <- "http://grch37.rest.ensembl.org"
ext <- paste0("/ld/human/",s_r,"/1000GENOMES:phase_3:EUR?d_prime=0.5&r2=0.5")
print(paste("fetching from ",server, ext, sep = ""))
r <- GET(paste(server, ext, sep = ""), content_type("application/json"))
stop_for_status(r)
df <- data.frame(fromJSON(toJSON(content(r))))
if(length(df)==0){
next
}

df <- as.data.frame(lapply(df, unlist), stringsAsFactors=F)
df <-df[rev(order(df$r2)),]
print(df)
for(i in 1:nrow(df))
{
  cur_rs <- df$variation2[i]  
  if(cur_rs %in% available.rsids){
      mapped.rsids[[s_r]] <- cur_rs
      print(paste0(s_r,"->",cur_rs))
      break 
  } 
}
}

print(mapped.rsids)
keys<-keys(mapped.rsids)
values<-values(mapped.rsids)
d<-cbind(keys,values)
h.df<-as.data.frame(d)
h.df<-data.frame(lapply(h.df, as.character), stringsAsFactors=F)
write.table(h.df, "rsid_proxies.txt", row.names=F, sep='\t')
