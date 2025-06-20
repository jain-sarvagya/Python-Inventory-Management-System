create database product;
use product;
create table category(
    c_id INT not null auto_increment,
    c_name varchar(20) not null,
    primary key(c_id));
CREATE TABLE sub_category (
    s_id INT NOT NULL AUTO_INCREMENT,
    s_name VARCHAR(20),
    c_id INT,
    PRIMARY KEY (s_id),
    FOREIGN KEY (c_id) REFERENCES category(c_id)
);
create table product(
    p_id INT auto_increment,
    p_name varchar(20),
    p_description varchar(50),
    s_id INT,
    making_date varchar(20),
    primary key(p_id),
    batch_no INT,
    foreign key(s_id) references sub_category(s_id));
create table inventory(
	p_id INT,
    p_name varchar(20),
	quantity INT,
    foreign key(p_id) references product(p_id));
create table customer(customer_id INT auto_increment,
	customer_name varchar(50),
	customer_pn INT,
    primary key(customer_id));
CREATE TABLE sales (
    sales_id INT auto_increment primary key,
    p_id INT,
    customer_id INT,
    units_purchased INT,
    stock_after_purchase INT);


