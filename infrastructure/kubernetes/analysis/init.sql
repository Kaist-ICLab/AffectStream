create table public.start_record
(
    id            bigserial    primary key,
    connection_id varchar(255) not null,
    timestamp     bigint       not null,
    response_time bigint       not null
);

create table public.end_record
(
    id             bigserial    primary key,
    connection_id  varchar(255) not null,
    timestamp      bigint       not null,
    inference_time bigint      not null
);
