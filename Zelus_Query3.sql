select 
  batter, 
  strike_rate, 
  runs_scored, 
  balls_faced 
  from
    (select 
	  batter,
      runs_scored,
      (total_balls - total_wides - total_noballs) as balls_faced,
      (runs_scored*100)/(total_balls - total_wides - total_noballs) strike_rate, 
      rank() over(order by (runs_scored*100)/(total_balls-total_wides-total_noballs) desc) as rank
      from
        (select batter, sum(batter_runs) as runs_scored, count(batter) as total_balls, sum(wides) as total_wides, sum(noballs) as total_noballs 
        from odi_ball_to_ball_details 
    where STRFTIME('%Y', match_date) = "2019" group by batter) totals)rt 
 where rt.rank=1;