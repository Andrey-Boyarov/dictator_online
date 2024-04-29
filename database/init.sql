create table questions (

    id serial primary key,
    prompt text, 
    faction text,

    confirm_crowd bigint, 
    confirm_oligarchs bigint,
    confirm_enforcement bigint,
    confirm_lawyers bigint,
    confirm_army bigint,
    confirm_mafia bigint,

    reject_crowd bigint,
    reject_oligarchs bigint, 
    reject_enforcement bigint, 
    reject_lawyers bigint, 
    reject_army bigint, 
    reject_mafia bigint,

    active boolean default true);
