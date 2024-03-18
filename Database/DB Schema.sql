CREATE DATABASE cs_item_history
    WITH
    OWNER = postgres
    ENCODING = 'UTF8'
    LOCALE_PROVIDER = 'libc'
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;

CREATE ROLE csa_application_role WITH
	LOGIN
	NOSUPERUSER
	NOCREATEDB
	NOCREATEROLE
	INHERIT
	NOREPLICATION
	NOBYPASSRLS
	CONNECTION LIMIT -1
	PASSWORD 'xxxxxxxxxxxxxxxx'; -- Change Password. Password should match in db.conf

CREATE TABLE buff163_data (
	market_hash_name VARCHAR(100) NOT NULL,
	buy_max_price FLOAT,
	buy_num INT,
	can_bargain BOOLEAN,
	"id" INT,
	market_min_price INT,
	quick_price FLOAT,
	sell_min_price FLOAT,
	sell_num FLOAT,
	sell_reference_price FLOAT,
	transacted_num INT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(market_hash_name, created_at, "id")
);

CREATE TABLE skinout_data (
	market_hash_name VARCHAR(100) NOT NULL,
    "id" INT,
    "float" FLOAT,
    stickers JSONB, 
    price FLOAT,
    "locked" BOOLEAN,
    unlock_time VARCHAR(20),
	total_count INT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(market_hash_name, created_at, "id")
);

CREATE TABLE skinport_data (
    market_hash_name VARCHAR(100) NOT NULL,
    suggested_price FLOAT,
    min_price FLOAT,
    max_price FLOAT,
    mean_price FLOAT,
    median_price FLOAT,
    quantity INT,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(market_hash_name, created_at)
);

CREATE TABLE steam_data (
	hash_name VARCHAR(100) NOT NULL,
    sell_listings INT,
    sell_price INT,
    sale_price_text VARCHAR(10),
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(hash_name, created_at)
);

GRANT INSERT, SELECT ON TABLE public.buff163_data TO csa_application_role;

GRANT INSERT, SELECT ON TABLE public.skinout_data TO csa_application_role;

GRANT INSERT, SELECT ON TABLE public.skinport_data TO csa_application_role;

GRANT INSERT, SELECT ON TABLE public.steam_data TO csa_application_role;