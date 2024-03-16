CREATE TABLE buff163_data (
	market_hash_name VARCHAR(100) NOT NULL PRIMARY KEY,
	buy_max_price FLOAT,
	buy_num INT,
	can_bargain BOOLEAN,
	"id" INT,
	market_min_price INT,
	quick_price FLOAT,
	sell_min_price FLOAT,
	sell_num FLOAT,
	sell_reference_price FLOAT,
	transacted_num INT
);

CREATE TABLE skinout_data (
	market_hash_name VARCHAR(100) NOT NULL PRIMARY KEY,
    "id" INT,
    "float" FLOAT,
    stickers JSONB, 
    price FLOAT,
    "locked" BOOLEAN,
    unlock_time BOOLEAN,
	total_count INT
);

CREATE TABLE skinport_data (
    market_hash_name VARCHAR(100) NOT NULL PRIMARY KEY,
    suggested_price FLOAT,
    min_price FLOAT,
    max_price FLOAT,
    mean_price FLOAT,
    median_price FLOAT,
    quantity INT,
    created_at INT, 
    updated_at INT 
);

CREATE TABLE steam_data (
	hash_name VARCHAR(100) NOT NULL PRIMARY KEY,
    "name" VARCHAR(100),
    sell_listings INT,
    sell_price INT,
    sell_price_text VARCHAR(20),
    sale_price_text VARCHAR(10)
);

GRANT INSERT, SELECT ON TABLE public.buff163_data TO csa_application_role;

GRANT INSERT, SELECT ON TABLE public.skinout_data TO csa_application_role;

GRANT INSERT, SELECT ON TABLE public.skinport_data TO csa_application_role;

GRANT INSERT, SELECT ON TABLE public.steam_data TO csa_application_role;