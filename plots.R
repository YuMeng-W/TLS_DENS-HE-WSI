#############################################
#################1-KM_curves#################
#Load Packages
library(survival)
library(survminer)
#Read data
df <- read.csv('data_train.csv')
##KM_curves plot
fit <- survfit(Surv(DFS_month, DFS) ~TLS_Dens, df)
ggsurvplot(fit, 
           data = df, 
           palette = c("#ED0000FF","#00468BFF"),
           pval = TRUE,
           pval.size = 5, 
           pval.coord = c(3.8,0.05),  
           legend = c(0.112,0.165),
           legend.title = "",
           legend.labs = c("TLS-low","TLS-high"),
           font.legend = 14,
           risk.table = TRUE, 
           risk.table.fontsize = 5,
           tables.theme = theme_cleantable(),
           xlab = "Time from surgery (months)",
           ylab = "Probability of \ndisease-free survival", 
           break.x.by = 12,  
           font.x = 16, 
           font.y = 16, 
           font.tickslab = c(14, "plain"), 
           axes.offset = FALSE, 
           ggtheme = theme_classic(base_size = 14))


#############################################
##########2-Coherence analysis###############
#Load Packages
library('lpSolve')
library('irr')
library(ggplot2)
library(blandr)
##ICC
df <- read.csv('data.csv')
icc(df, model = "twoway", type = "agreement")
##Bland-Altman Plots
label <- df$num_tls_HE
# label <- df$num_tls_IHC
auto <- df$num_tls_auto
stats <- blandr.statistics(label, auto)
mean_diff <- mean(stats$differences)
lower <- mean_diff - 1.96* sd(stats$differences)
upper <- mean_diff + 1.96* sd(stats$differences)
XX <- stats$means
YY <- stats$differences
ggplot(dat, aes(x=XX, y=YY))+
  geom_point(size = 3, shape =1, color = 'black',stroke = 1)+
  geom_hline(yintercept = mean_diff,color = '#ED0000FF', linetype = 'solid', size=1)+
  geom_hline(yintercept = lower, color= '#00468BFF', linetype = 'dashed', size = 1)+
  geom_hline(yintercept = upper, color = '#00468BFF', linetype = 'dashed', size = 1)+
  ylab('Difference between manual counting \nand automated counting')+
  xlab('Mean of manual counting and automated counting')+
  theme_classic()+ ylim(-25, 35) +
  theme(axis.line = element_line(linetype = "solid", linewidth =0.8),
        axis.title = element_text(size = 18),
        axis.text = element_text(size = 14,colour = "gray20"),
        panel.background = element_rect(fill = NA))

#############################################
#################3-Bar_Plot#################
#Load Packages
library(ggplot2)
library(tidyr)
library("RColorBrewer")
#Read data
df <- read.csv("data.csv")
dat1 <- gather(df, level, perc, -IPs)
#Plots
ggplot(dat1, aes(IPs, perc, fill = level)) +
  geom_bar(stat = "identity", position = "fill", width = 0.8) +
  scale_fill_manual(values = c("#00468BFF","#ED0000FF")) +
  labs(x = " ", y = " ") + 
  scale_y_continuous(expand = c(0,0.004)) +
  theme(axis.title = element_text(size = 18), 
        axis.text = element_text(color = "black"),
        axis.text.x = element_blank(),
        axis.text.y = element_text(size = 12), 
        # axis.line = element_line(size = 0.5),  
        axis.line.y.right = element_line(color = "red"),
        panel.background = element_rect(fill = "white", colour = "black", linewidth = 1.2),
        panel.grid = element_blank(),       
        # legend.position = "none",
        legend.title = element_blank(),     
        legend.justification = c(1,0.95)   
  )

#############################################
#################4-Violin_Plot#################
#Load Packages
library(ggplot2)
library(gridExtra)
#Read data
df <- read.csv('data_tr.csv')
#Normal distribution
hist(df$tls_density, prob = T)
xfit <- seq(min(df$tls_density), max(df$tls_density), length = 20)
yfit <- dnorm(xfit, mean(df$tls_density), sd(df$tls_density))
lines(xfit, yfit, col = "red", lwd = 2)
lines(density(df$tls_density), col = "blue", lwd = 2)
shapiro.test(df$tls_density)
#Plot
ggplot(df, aes(x= TNM_Stage, y= tls_density, fill = TNM_Stage))+
  geom_violin(trim = F) +    
  scale_fill_manual(values = c("#00468BFF", "#ED0000FF", "#42B540FF")) +   
  geom_boxplot(width = 0.08, fill = "white" ,
               outlier.alpha = 0) +
  theme_bw()+
  theme(axis.text.x = element_text(color = 'black',size = 16,face = "italic"),
        axis.text.y = element_text(color = 'black',size = 14),   
        axis.title = element_text(size =18),
        axis.title.x = element_blank(),   
        panel.grid = element_blank(),   
        panel.grid.major = element_line(colour = NA),
        panel.grid.minor = element_line(colour = NA),
        panel.background = element_rect(fill = NA, colour = 'black', size = 1),
        legend.position = 'none')     









