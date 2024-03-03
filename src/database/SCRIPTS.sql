CREATE SEQUENCE seq_paciente
  START WITH 1
  INCREMENT BY 1
  MAXVALUE 999;

CREATE SEQUENCE seq_espe
  START WITH 1
  INCREMENT BY 1
  MAXVALUE 999;

CREATE SEQUENCE seq_comida 
  START WITH 1
  INCREMENT BY 1
  MAXVALUE 999;

CREATE SEQUENCE seq_alimento
  START WITH 1
  INCREMENT BY 1 
  MAXVALUE 999;

  
CREATE TABLE pacientes ( 
	id_paciente 			numeric(3) 		PRIMARY KEY     DEFAULT NEXTVAL('seq_paciente'),
	pri_nombre   			varchar(40) 	NOT NULL,
	pri_apellido   			varchar(40) 	NOT NULL,
    seg_apellido  			varchar(40) 	NOT NULL,
	sexo 					varchar(1) 		NOT NULL        CHECK(sexo IN ('F','M','O')),
    correo                  varchar(40) 	NOT NULL        UNIQUE,
	telefono                numeric(17)     NOT NULL,
    clave                   varchar(255) 	NOT NULL,
    fecha_nacimiento 		date			NOT NULL,
    seg_nombre  			varchar(40)
);

CREATE TABLE especialistas ( 
	id_espe      			numeric(3) 		PRIMARY KEY     DEFAULT NEXTVAL('seq_espe'),
	pri_nombre   			varchar(40) 	NOT NULL,
	pri_apellido   			varchar(40) 	NOT NULL,
    seg_apellido  			varchar(40) 	NOT NULL,
	sexo 					varchar(1) 		NOT NULL        CHECK(sexo IN ('F','M','O')),
    correo                  varchar(40) 	NOT NULL        UNIQUE,
	telefono                numeric(17)     NOT NULL,
    clave                   varchar(255) 	NOT NULL,
    especialidad            varchar(80)		NOT NULL,
    seg_nombre  			varchar(40)
);

CREATE TABLE alimentos (
    id_alimento 			numeric(3) 		PRIMARY KEY DEFAULT NEXTVAL('seq_alimento'),
    tipo                    varchar(15)     NOT NULL    CHECK(tipo IN ('Proteina','Carbohidrato','Grasa','Vegetal','Fruta','Lacteo','Bebida','Dulce','Salado','Otros')),
    nombre                  varchar(40)     NOT NULL,
    cantidad                numeric(10)     NOT NULL
);

CREATE TABLE comidas (
    id_paciente             numeric(3)      NOT NULL,
    id_espe                 numeric(3)      NOT NULL,
    id_comida 				numeric(3)      NOT NULL    DEFAULT NEXTVAL('seq_comida'),
    tipo 	                varchar(1) 	    NOT NULL    CHECK(tipo IN ('D','A','C','M')),
    FOREIGN KEY (id_paciente) REFERENCES pacientes(id_paciente),
    FOREIGN KEY (id_espe) REFERENCES especialistas(id_espe),
    PRIMARY KEY (id_paciente, id_espe, id_comida)
);

CREATE TABLE hist_comida (
    id_paciente             numeric(3)      NOT NULL,
    id_espe                 numeric(3)      NOT NULL,
    id_comida               numeric(3)      NOT NULL,
    fecha_ini               date            NOT NULL,
    satisfaccion   			varchar(40) 	NOT NULL    CHECK(satisfaccion IN ('Cansado','Mal','No muy bien','Normal','Bien', 'Super')), 
    comentario  			varchar(40),
    fecha_fin               date,
    FOREIGN KEY (id_paciente, id_espe, id_comida) REFERENCES comidas(id_paciente, id_espe, id_comida),
    PRIMARY KEY (id_paciente, id_espe, id_comida, fecha_ini)
);

CREATE TABLE a_c ( 
    id_paciente             numeric(3)      NOT NULL,
    id_espe                 numeric(3)      NOT NULL,
    id_comida               numeric(3)      NOT NULL,
    id_alimento             numeric(3)      NOT NULL,
    FOREIGN KEY (id_paciente, id_espe, id_comida) REFERENCES comidas(id_paciente, id_espe, id_comida),
    FOREIGN KEY (id_alimento) REFERENCES alimentos(id_alimento),
    PRIMARY KEY (id_paciente, id_espe, id_comida, id_alimento)
);