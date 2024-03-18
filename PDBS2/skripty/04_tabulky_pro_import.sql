-- Table: public.obyvatele_roky

-- DROP TABLE IF EXISTS public.obyvatele_roky;

CREATE TABLE IF NOT EXISTS public.obyvatele_roky
(
    idhod integer,
    hodnota integer,
    stapro_kod integer,
    pohlavi_cis boolean,
    pohlavi_kod boolean,
    vek_cis boolean,
    vek_kod boolean,
    uzemi_cis integer,
    uzemi_kod integer,
    obdobi text COLLATE pg_catalog."default",
    pohlavi_txt boolean,
    vek_txt boolean,
    uzemi_txt text COLLATE pg_catalog."default",
    uzemi_typ text COLLATE pg_catalog."default"
)

CREATE TABLE IF NOT EXISTS public.ciselnik_csu_ruian
(
    typ text,
    kod_csu integer,
    kod_ruian integer
)