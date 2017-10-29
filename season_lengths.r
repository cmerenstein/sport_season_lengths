library(ggplot2)
library(dplyr)
library(tidyr)

colors = c("#2491ff", "green", "#F27371", "purple")

nhl = read.csv("nhl/NHL_r_squared_table.csv") %>% 
  rename(NHL = r_squared) %>% 
  mutate(percent_of_season = game/82)
nba = read.csv("nba/NBA_r_squared_table.csv") %>% 
  rename(NBA = r_squared) %>% 
  mutate(percent_of_season = game/82)
nfl = read.csv("nfl/NFL_r_squared_table.csv") %>% 
  rename(NFL = r_squared) %>% 
  mutate(percent_of_season = game/16)
mlb = read.csv("mlb/MLB_r_squared_table.csv") %>% 
  rename(MLB = r_squared) %>% 
  mutate(percent_of_season = game/162)

leagues_percent = full_join(nhl, nba, by="percent_of_season") %>% 
  full_join( nfl, by="percent_of_season") %>% 
  full_join( mlb, by="percent_of_season") %>% 
  gather(league, r_squared, `NHL`, `NBA`, `NFL`, `MLB`) 

leagues_percent = leagues_percent[,c("league", "r_squared", "percent_of_season")] %>% 
  filter(!is.na(r_squared))

ggplot(data=leagues_percent, aes(x = percent_of_season, y = r_squared, color = league)) +
  geom_point(shape=21, size = 1, stroke = 1) + stat_smooth(se=F) + 
  theme_bw() + theme(panel.border = element_blank()) + 
  scale_color_manual(values = colors)

leagues_by_game = full_join(nhl, nba, by="game") %>% 
  full_join( nfl, by="game") %>% 
  full_join( mlb, by="game") %>% 
  gather(league, r_squared, `NHL`, `NBA`, `NFL`, `MLB`)

leagues_by_game = leagues_by_game[,c("league", "r_squared", "game")] %>% 
  filter(!is.na(r_squared))


ggplot(data=leagues_by_game, aes(x = game, y = r_squared, color = league)) +
  geom_point() + stat_smooth() + 
  theme_bw() + theme(panel.border = element_blank()) + 
  scale_color_manual(values = colors)
