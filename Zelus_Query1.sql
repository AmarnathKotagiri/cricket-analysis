select 
  tm.team_name, 
  tm.year, 
  tm.gender, 
  case when tw.total_wins then tw.total_wins else 0 end AS "wins_per_year", 
  tm.matches_per_year, 
  ((case when tw.total_wins then tw.total_wins else 0 end)*100)/tm.matches_per_year AS "win_percentage"
  from
    (select strftime('%Y', match_date) AS "year", gender, winner, count(winner) AS "total_wins"
      from odi_match_details where result = "Completed"
      group by year, gender, winner) tw
    right outer join 
    (select team_name, year, gender, sum(count1) AS matches_per_year from
        (select team_name, year, gender, count1 from 
          (select team_name  from odi_team_details group by 1) otd
          inner join 
          (select strftime('%Y', match_date) AS "year", gender, team1 AS "team", count(team1) AS "count1"
            from odi_match_details where result = "Completed"
            group by year, gender, team) a
          on otd.team_name=a.team
        union all
        select team_name, year, gender, count1 from 
          (select team_name  from odi_team_details group by 1) otd
          inner join
          (select strftime('%Y', match_date) AS "year", gender, team2 AS "team", count(team2) AS "count1"
            from odi_match_details where result = "Completed"
            group by year, gender, team) b
          on otd.team_name=b.team ) x 
	group by team_name, year, gender) tm
  on tw.winner = tm.team_name and tw.gender = tm.gender and tw.year = tm.year
order by tm.year asc; 