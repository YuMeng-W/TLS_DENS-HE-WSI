###########################################
##########Survival analysis################
#Load Packages
library(broom)
library(glmnet)
library(cutoff)
library(ggpubr)
library(survival)
library(tableone)
library(openxlsx)
library(survminer)
##Discovery
#Read data
data_train <- read.csv("data_tr.csv")
#cut-off 
res_cut <- surv_cutpoint(data_train, time='DFS_month', event='DFS', variables=c('tls_density'))
cutpoint = summary(res_cut)$cutpoint[1]
#Categorize variable 
tmp0 <- data_train$tls_density > cutpoint
TLS_Dens_tr <- as.vector(ifelse(tmp0, "1", "0"))
data_train$TLS_Dens <- TLS_Dens_tr
#Univariable analysis
data_train$TLS_Dens <- factor(data_train$TLS_Dens)    
res.cox <- coxph(Surv(DFS_month, DFS) ~TLS_Dens, data = data_train)
sum.cox <- summary(res.cox)
#Multivariable analysis
#factors
fvars <- c('sex', 'smoking', 'tumor_differentiation', 'AJCC_stage',
           'IP', 'TLS_Dens', 'VPI','LVI','adjuvant_chemotherapy','surgery_mode') 
data_train[fvars]<-lapply(data_train[fvars],factor)
#Build Model
f1 <- coxph(Surv(DFS_month, DFS) ~smoking+tumor_differentiation+AJCC_stage+LVI+TLS_Dens, 
           data = data_train) 
f1_step <- step(f1)
#f1_step <- f1
summary(f1_step)
f1_aic_tr <- AIC(f1_step)   #AIC

##External Validation
#Read data
data_valid <- read.csv("data_vd.csv")
#Categorize variable 
tmp1 <- data_valid$tls_density > cutpoint
TLS_Dens_vd <- as.vector(ifelse(tmp1, "1", "0"))
data_valid$TLS_Dens <- TLS_Dens_vd
#Univariable analysis
data_valid$TLS_Dens <- factor(data_valid$TLS_Dens)    
res.cox <- coxph(Surv(DFS_month, DFS) ~TLS_Dens, data = data_valid)
sum.cox <- summary(res.cox)
#Multivariable analysis
#factors
fvars <- c('sex', 'smoking', 'tumor_differentiation', 'AJCC_stage',
           'IP', 'TLS_Dens', 'VPI','LVI','adjuvant_chemotherapy','surgery_mode') 
data_valid[fvars]<-lapply(data_valid[fvars],factor)
#Build Model
f2_CI <- summary(coxph(Surv(data_valid$DFS_month, data_valid$DFS) ~predict(f1_step, 
                        data_valid), data_valid))$concordance
f2 <- coxph(Surv(DFS_month, DFS) ~smoking+tumor_differentiation+AJCC_stage+LVI+TLS_Dens, 
            data = data_valid) 
f2_step <- step(f2)
#f2_step <- f2
summary(f2_step)
f2_aic_vd <- AIC(f2_step)   #AIC

