# Fighter:
    fighter_id (int, primary key)
    name (string)
    nickname (string, nullable)
    birth_date (date)
    height_in (float)
    reach_in (float, nullable)
    stance (string) (Orthodox, Southpaw, Switch)
    weight_class (string) (Flyweight -> Heavyweight)
    debut_date (date, nullable)

# Fight:
    fight_id (int, primary key)
    event_name (string)
    event_date (date)
    weight_class (string)
    rounds_scheduled (int) (3 for normal, 5 for main event/championship)
    referee (string, nullable)

# Fighter Fight Stats:
    Fight_stats

    fight_id (int, foreign key)
    fighter_id (int, foreign key)
    opponent_id (int, foreign key)
    result (string) (Win, Loss, Draw, No Contest)
    method (string) (KO/TKO, Submission, Decision)
    round_finished (int, nullable)
    time_finished_sec (int, nullable)

    Striking

    sig_str_landed (int)
    sig_str_attempted (int)
    total_str_landed (int)
    total_str_attempted (int)
    knockdowns (int)

    Grappling

    takedowns_landed (int)
    takedowns_attempted (int)
    submission_attempts (int)
    control_time_sec (int)