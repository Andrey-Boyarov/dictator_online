create table questions (

    id bigint primary key,
    prompt text, 

    confirm_crowd bigint, 
    confirm_oligarchs bigint,
    confirm_enforcment bigint,
    confirm_lawyers bigint,
    confirm_army bigint,
    confirm_mafia bigint,

    reject_crowd bigint,
    reject_oligarchs bigint, 
    reject_enforcment bigint, 
    reject_lawyers bigint, 
    reject_army bigint, 
    reject_mafia bigint,
    
    is_relevant boolean default true);
