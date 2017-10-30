library(ggplot2)
library(dplyr)
library(tidyr)

colors_leagues = c("#2491ff", "green", "#F27371", "purple")
colors_nba = c("#2491ff", "green", "#F27371", "#c6a500", "purple")

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
  geom_point(shape=21, size = 1.5) + stat_smooth(se=F) + 
  theme_bw() + theme(panel.border = element_blank()) + 
  scale_color_manual(values = colors_leagues) + 
  xlab("Percent of Season") 
  

leagues_by_game = full_join(nhl, nba, by="game") %>% 
  full_join( nfl, by="game") %>% 
  full_join( mlb, by="game") %>% 
  gather(league, r_squared, `NHL`, `NBA`, `NFL`, `MLB`)

leagues_by_game = leagues_by_game[,c("league", "r_squared", "game")] %>% 
  filter(!is.na(r_squared))

ggplot(data=leagues_by_game, aes(x = game, y = r_squared, color = league)) +
  geom_point() + stat_smooth() + 
  theme_bw() + theme(panel.border = element_blank()) + 
  scale_color_manual(values = colors_leagues)




### testing NBA lengths

nba_20 = read.csv("nba/NBA_r_squared_table_20.csv") %>% 
  rename(NBA_20 = r_squared) %>% 
  mutate(percent_of_season = game/20)

nba_41 = read.csv("nba/NBA_r_squared_table_41.csv") %>% 
  rename(NBA_41 = r_squared) %>% 
  mutate(percent_of_season = game/41)

nba_62 = read.csv("nba/NBA_r_squared_table_62.csv") %>% 
  rename(NBA_62 = r_squared) %>% 
  mutate(percent_of_season = game/62)

nba_82 = read.csv("nba/NBA_r_squared_table.csv") %>% 
  rename(NBA_82 = r_squared) %>% 
  mutate(percent_of_season = game/82)


nba_variations_percent = full_join(nhl, nba_82, by="percent_of_season") %>% 
  full_join( nba_62, by="percent_of_season") %>% 
  full_join( nba_41, by="percent_of_season") %>% 
  full_join( nba_20, by="percent_of_season") %>% 
  gather(league, r_squared, `NHL`, `NBA_82`, `NBA_62`, `NBA_41`, `NBA_20`) 

nba_variations_percent = nba_variations_percent[,c("league", "r_squared", "percent_of_season")] %>% 
  filter(!is.na(r_squared))

ggplot(data=nba_variations_percent, aes(x = percent_of_season, y = r_squared, color = league)) +
  geom_point(shape=21, size = 1.5) + stat_smooth(se=F) + 
  theme_bw() + theme(panel.border = element_blank()) + 
  scale_color_manual(values = colors_nba) + 
  xlab("Percent of Season") 


#### Simulated seasons

simulated_seasons_list = list.files(path="simulated_seasons", pattern="\\.csv")
files = paste("simulated_seasons", simulated_seasons_list, sep="/")
seasons = lapply(files, read.csv, header=T)

simulated_season_rvalues = do.call(rbind, seasons) %>% 
  mutate(percent_of_season = games/82) %>% 
  mutate(odds.better.team.wins = as.character(odds.better.team.wins))

ggplot(data=simulated_season_rvalues, aes(x = percent_of_season, y = r_squared, color = odds.better.team.wins)) +
  geom_point(shape=21, size = 1.5) + stat_smooth(se=F) + 
  theme_bw() + theme(panel.border = element_blank())


sim_60 = read.csv("simulated_seasons/simulated_60.csv") %>% 
  mutate(percent_of_season = games/82) %>% 
  rename(league = odds.better.team.wins) %>% 
  mutate(league = "Simulated 0.6") %>% 
  mutate(game = games) %>% 
  select(`game`, `r_squared`, `percent_of_season`, `league`)


sim_70 = read.csv("simulated_seasons/simulated_70.csv") %>% 
  mutate(percent_of_season = games/82) %>% 
  rename(league = odds.better.team.wins) %>% 
  mutate(league = "Simulated 0.7") %>% 
  mutate(game = games) %>% 
  select(`game`, `r_squared`, `percent_of_season`, `league`)

nhl = read.csv("nhl/NHL_r_squared_table.csv") %>% 
  mutate(league = "NHL") %>% 
  mutate(percent_of_season = game/82)

nba = read.csv("nba/NBA_r_squared_table.csv") %>% 
  mutate(league = "NBA") %>% 
  mutate(percent_of_season = game/82)


nba_nhl_simulated = do.call(rbind, list(sim_60, sim_70, nba, nhl))

ggplot(data=nba_nhl_simulated, aes(x = percent_of_season, y = r_squared, color = league)) +
  geom_point(shape=21, size = 1.5) + stat_smooth(se=F) + 
  theme_bw() + theme(panel.border = element_blank()) +
  xlab("Percent of Season") 



