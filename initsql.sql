/* CREATE DATABASE */
/*CREATE DATABASE IF NOT EXISTS ERMS_TEAM49; USE ERMS_TEAM49;*/

/* CREATE USERS TABLE */

DROP TABLE IF EXISTS USERS;
CREATE TABLE IF NOT EXISTS USERS(
USERNAME VARCHAR(50) NOT NULL,
PASSWORD VARCHAR(50) NOT NULL,
NAME VARCHAR(150) NOT NULL,
primary key (USERNAME)
);

/* CREATE INDIVIDUAL_USERS TABLE */
DROP TABLE IF EXISTS INDIVIDUAL_USERS;
CREATE TABLE IF NOT EXISTS INDIVIDUAL_USERS( USERNAME VARCHAR(50) NOT NULL,
JOBTITLE VARCHAR(150) NOT NULL,
DATEOFHIRE DATE NOT NULL,
primary key (USERNAME),
foreign key (USERNAME)
REFERENCES USERS(USERNAME)
    ON DELETE CASCADE
ON UPDATE CASCADE
);

/*CREATE MUNICIPALITY_USERS TABLE*/
DROP TABLE IF EXISTS MUNICIPALITY_USERS;
CREATE TABLE IF NOT EXISTS MUNICIPALITY_USERS( USERNAME VARCHAR(50) NOT NULL,
POPULATION INT NOT NULL,
primary key (USERNAME),
foreign key (USERNAME)
REFERENCES USERS(USERNAME)
    ON DELETE CASCADE
ON UPDATE CASCADE
);

/* CREATE GOVAGENCY_USERS TABLE*/
DROP TABLE IF EXISTS GOVAGENCY_USERS;
CREATE TABLE IF NOT EXISTS GOVAGENCY_USERS( USERNAME VARCHAR(50) NOT NULL,
JURISDICTION VARCHAR(255) NOT NULL,
primary key (USERNAME),
foreign key (USERNAME)
REFERENCES USERS(USERNAME)
    ON DELETE CASCADE
ON UPDATE CASCADE
);

/* CREATE COMPANY_USERS TABLE*/
DROP TABLE IF EXISTS COMPANY_USERS;
CREATE TABLE IF NOT EXISTS COMPANY_USERS(
USERNAME VARCHAR(50) NOT NULL,
LOC_OF_HQ VARCHAR(255) NOT NULL,
primary key (USERNAME),
foreign key (USERNAME)
REFERENCES USERS(USERNAME)
    ON DELETE CASCADE
ON UPDATE CASCADE
);

/* CREATE INCIDENT TABLE*/
DROP TABLE IF EXISTS INCIDENTS;
CREATE TABLE IF NOT EXISTS INCIDENTS(
INC_ID int NOT NULL AUTO_INCREMENT,
USERNAME VARCHAR(50) NOT NULL,
DESCRIPTION VARCHAR(255) NOT NULL,
LATITUDE DECIMAL(9,6) NOT NULL,
LONGITUDE DECIMAL(9,6) NOT NULL,
primary key (INC_ID),
foreign key (USERNAME)
REFERENCES USERS(USERNAME)
    ON DELETE CASCADE
ON UPDATE CASCADE
);

/* CREATE ESF TABLE*/
DROP TABLE IF EXISTS ESF;
CREATE TABLE IF NOT EXISTS ESF(
ESF_ID INT NOT NULL,
DESCRIPTION VARCHAR(255) NOT NULL,
primary key (ESF_ID)
);

/* CREATE COST_PER TABLE*/
DROP TABLE IF EXISTS COST_PER;
CREATE TABLE IF NOT EXISTS COST_PER(
COSTPER VARCHAR(50) NOT NULL,
primary key (COSTPER)
);

/* CREATE RESOURCE TABLE*/
DROP TABLE IF EXISTS RESOURCE;
CREATE TABLE IF NOT EXISTS RESOURCE(
ID int NOT NULL AUTO_INCREMENT,
USERNAME VARCHAR(50) NOT NULL,
NAME VARCHAR(50) NOT NULL,
P_ESF INT,
M_NAME VARCHAR(50) NULL, #MODEL NAME
AMOUNT DECIMAL NOT NULL,
COST_PER VARCHAR(50) NOT NULL,
STATUS VARCHAR(255) NOT NULL,
DATE_AV DATE NOT NULL, # DATE AVAILABLE
LATITUDE DECIMAL(9,6) NOT NULL,
LONGITUDE DECIMAL(9,6) NOT NULL,
primary key (ID),
foreign key (USERNAME)
REFERENCES USERS(USERNAME)
    ON DELETE CASCADE
ON UPDATE CASCADE,
foreign key (P_ESF)
REFERENCES ESF(ESF_ID)
    ON DELETE CASCADE
ON UPDATE CASCADE,
foreign key (COST_PER)
REFERENCES COST_PER(COSTPER)
    ON DELETE CASCADE
ON UPDATE CASCADE
);

/* CREATE RESOURCE_CAPABILTY TABLE*/
DROP TABLE IF EXISTS RESOURCE_CAPABILTY;
CREATE TABLE IF NOT EXISTS RESOURCE_CAPABILTY( RES_ID INT NOT NULL,
CAPABILITY VARCHAR(255) NOT NULL,
primary key (RES_ID,CAPABILITY),
foreign key (RES_ID)
REFERENCES RESOURCE(ID)
    ON DELETE CASCADE
ON UPDATE CASCADE
);

/* CREATE ADDITIONAL_ESF TABLE*/
DROP TABLE IF EXISTS ADDITIONAL_ESF;
CREATE TABLE IF NOT EXISTS ADDITIONAL_ESF(
RES_ID INT NOT NULL,
ESF_ID INT NOT NULL,
primary key (RES_ID,ESF_ID),
foreign key (RES_ID)
REFERENCES RESOURCE(ID)
    ON DELETE CASCADE
ON UPDATE CASCADE,
foreign key (ESF_ID)
REFERENCES ESF(ESF_ID)
    ON DELETE CASCADE
ON UPDATE CASCADE
);

/* CREATE ADDITIONAL_ESF TABLE*/
DROP TABLE IF EXISTS ADDITIONAL_ESF;
CREATE TABLE IF NOT EXISTS ADDITIONAL_ESF(
RES_ID INT NOT NULL,
ESF_ID INT NOT NULL,
primary key (RES_ID,ESF_ID),
foreign key (RES_ID)
REFERENCES RESOURCE(ID)
    ON DELETE CASCADE
ON UPDATE CASCADE,
foreign key (ESF_ID)
REFERENCES ESF(ESF_ID)
    ON DELETE CASCADE
ON UPDATE CASCADE
);

/* CREATE REQUESTS TABLE*/
DROP TABLE IF EXISTS REQUESTS;
CREATE TABLE IF NOT EXISTS REQUESTS(
RES_ID INT NOT NULL,
INC_ID INT NOT NULL,
REQ_DATE DATE NOT NULL,
RET_DATE DATE NOT NULL,
STATUS VARCHAR(25),
APP_DATE DATE,
primary key (RES_ID,INC_ID),
foreign key (RES_ID)
REFERENCES RESOURCE(ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
foreign key (INC_ID)
REFERENCES INCIDENTS(INC_ID)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

/* CREATE REP_REQUESTS TABLE*/
DROP TABLE IF EXISTS REP_REQUESTS;
CREATE TABLE IF NOT EXISTS REP_REQUESTS(
RES_ID INT NOT NULL,
START_DATE DATE NOT NULL,
READY_DATE DATE NOT NULL,
primary key (RES_ID),
foreign key (RES_ID)
REFERENCES RESOURCE(ID)
    ON DELETE CASCADE
ON UPDATE CASCADE
);