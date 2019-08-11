install.packages("gganimate")
install.packages("gifski")
install.packages("ggthemes")
install.packages("tidyverse")
install.packages("extrafont")

# loading required libraries
library(ggplot2)
library(gganimate)
library(gifski)
library(ggthemes)
library(reshape2)
library(tidyverse)
library(extrafont)

#font_import(pattern = "Nanum")
# 폰트
# https://statkclee.github.io/viz/viz-r-font.html
# 위의 사이트 참조해서 리눅스에도 글꼴 설치 
#library(showtext)
#font_add_google("Nanum Gothic")
# 그래프 한글 깨짐문제 해결
theme_set(theme_gray(base_family="NanumGothicCoding"))

#loading_dataset
movie_data<-read.csv("/Users/Shinwoohyun/Desktop/Github/ML_Projet/ML_Projet/portfolio/cine.csv",header= TRUE, stringsAsFactors=FALSE)

#selecting columns to work with
movie_sub<-movie_data %>% select("date","movieNm","audiAcc")

# pre-processing by week 일단 여기서 전처리 할 필요 없는듯
movie_sub_week1 <- movie_sub %>% filter(date ==20190102) %>% select("movieNm","audiAcc")
movie_sub_week2 <- movie_sub %>% filter(date ==20190109) %>% select("movieNm","audiAcc")
movie_sub_week3 <- movie_sub %>% filter(date ==20190116) %>% select("movieNm","audiAcc")
#....

#function to sum the total audience per movie
n<-unique(movie_sub_week1$movieNm)
movieNm <- function(x){
    movie1<-movie_sub_week1 %>% filter(movieNm==x)
    sum(movie1$audiAcc)
}

#return a list with all total audience per movie
audience_total<-sapply(n,function(x) movieNm(x))

#creating a dataframe with top 10 total audience per movie
df <- do.call(rbind,Map(data.frame,movieNm=n,Total_audience=audience_total))
df2<- df %>% arrange(desc(Total_audience))
df3<- head(df2,n=10)
write.csv(df3,"/Users/Shinwoohyun/Desktop/Github/ML_Projet/ML_Projet/portfolio/movie_sub.csv")

#plotting the top 10 movies leading in the total audience rates
ggplot(df3,aes(reorder(movieNm,Total_audience),Total_audience,fill=as.factor(movieNm)))+
           geom_col()+
           coord_flip(clip="off", expand= FALSE)+
           guides(fill=FALSE)+
           labs(title="TOTAL AUDIENCE PER MOVIE FROM 2019-2019",
                y="Total Audience per movie", x="MovieName")+
           scale_y_continuous(labels = scales::comma)+
           geom_text(aes(label = paste(Total_audience,"")), hjust =1)

sm4<-movie_sub %>% group_by(date) %>% mutate(rank = min_rank(-audiAcc)*1) %>% ungroup()
#geom_text(aes(y = 0, label = paste(movieNm, " ")), vjust = 0.2, hjust = 1)
#plotting static plot
static_plot<-ggplot(sm4,aes(rank,group=movieNm,fill=as.factor(movieNm),color=as.factor(movieNm))) +
    geom_tile(aes(y = audiAcc/2,
                  height = audiAcc,
                  width = 0.9), alpha = 0.8, color = NA) +
    geom_text(aes(y = 0, label = paste(movieNm, " "), family="NanumGothicCoding"), vjust = 0.2, hjust = 1) +
    geom_text(aes(y=audiAcc,label = paste(" ",audiAcc)), hjust=0)+
    coord_flip(clip = "off", expand = TRUE) +
    scale_y_continuous(labels = scales::comma) +
    scale_x_reverse() +
    guides(color = FALSE, fill = FALSE) +
    theme_minimal() +
    theme(
        plot.title=element_text(size=25, hjust=0.5, face="bold", colour="grey", vjust=-1),
        plot.subtitle=element_text(size=18, hjust=0.5, face="bold", color="grey"),
        plot.caption =element_text(size=8, hjust=0.5, face="bold", color="grey"),
        axis.ticks.y = element_blank(), 
        axis.text.y = element_blank(),
        plot.margin = margin(1,1,1,4, "cm")
    )

#creating final animation
plt<-static_plot + transition_states(states = date, transition_length = 4, state_length = 1) + 
    ease_aes('cubic-in-out') +
    #view_follow(fixed_x = TRUE) +
    labs(title = 'Total audience per week : {closest_state}', 
         subtitle = "Top 10 Movies",
         caption = "Data Source: KOBIS",
         x="Movies",y="Total Audience per week")

#rendering the animation for gif
final_animation<-animate(plt,100,fps = 20,duration = 30, width = 950, height = 750, renderer = gifski_renderer())

#saving the animation
anim_save("/Users/Shinwoohyun/Desktop/Github/ML_Projet/ML_Projet/portfolio/static/img/cinema.gif",animation=final_animation)
