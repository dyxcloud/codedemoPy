create table bgm_subject
(
    subject_id integer not null
        constraint bgm_subject_pk
            primary key,
    name varchar not null,
    name_cn varchar,
    point double precision default 0.0,
    rank integer default 0,
    votes integer default 0,
    date varchar,
    wanted integer default 0,
    watched integer default 0,
    watching integer default 0,
    hold integer default 0,
    "drop" integer default 0,
    create_date varchar
);


select subject_id from bgm_subject where subject_id=302189;
