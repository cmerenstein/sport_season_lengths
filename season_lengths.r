library(ggplot2)
library(dplyr)
library(tidyr)

colors = c("#2491ff", "green", "#F27371")

nhl = read.csv("nhl/NHL_r_squared_table.csv") %>% 
  rename(NHL = r_squared) %>% 
  mutate(percent_of_season = game/82)
nba = read.csv("nba/NBA_r_squared_table.csv") %>% 
  rename(NBA = r_squared) %>% 
  mutate(percent_of_season = game/82)
nfl = read.csv("nfl/NFL_r_squared_table.csv") %>% 
  rename(NFL = r_squared) %>% 
  mutate(percent_of_season = game/16)

leagues = full_join(nhl, nba, by="percent_of_season") %>% 
  full_join( nfl, by="percent_of_season") %>% 
  gather(league, r_squared, `NHL`, `NBA`, `NFL`) %>% 
  filter(!is.na(r_squared))

ggplot(data=leagues, aes(x = percent_of_season, y = r_squared, color = league)) +
  geom_point() + stat_smooth() + 
  theme_bw() + theme(panel.border = element_blank()) + 
  scale_color_manual(values = colors)