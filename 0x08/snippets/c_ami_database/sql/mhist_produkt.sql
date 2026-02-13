create table produkt
(
    id             int auto_increment
        primary key,
    bezeichnung    varchar(100)   null,
    warengruppe_id int            not null,
    einheit        varchar(20)    null,
    stueckpreis    decimal(12, 2) null,
    umsatzsteuer   decimal(6, 2)  null,
    constraint fk_produkt_warengruppe
        foreign key (warengruppe_id) references warengruppe (id)
)
    charset = utf8;

create index fk_produkt_warengruppe_idx
    on produkt (warengruppe_id);

INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (1, 'Spinat', 1, 'PK', 1.99, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (2, 'Vier Käse Pizza', 1, 'ST', 2.39, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (3, 'Spinatpizza', 1, 'ST', 2.29, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (4, 'Fischstäbchen', 1, 'PK', 1.99, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (5, 'Nudelpfanne', 1, 'PK', 3.29, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (6, 'Möhren', 2, 'KG', 0.39, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (7, 'Zwiebeln', 2, 'KG', 0.29, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (8, 'Bananen', 2, 'KG', 1.29, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (9, 'Knoblauch', 2, 'KG', 0.98, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (10, 'Fleischwurst', 3, 'ST', 1.99, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (11, 'Frikadellen', 3, 'PK', 2.35, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (12, 'Milch', 4, 'ST', 0.79, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (13, 'Quark', 4, 'ST', 0.99, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (14, 'Joghurt', 4, 'ST', 0.98, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (15, 'Cola light', 5, 'ST', 1.50, 0.19);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (16, 'Nerd Bull', 5, 'ST', 1.50, 0.19);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (17, 'Eistee', 5, 'ST', 1.80, 0.19);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (18, 'Wasser', 5, 'ST', 0.99, 0.19);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (19, 'Grillwürstchen', 6, 'PK', 3.55, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (20, 'Leberkäse', 6, 'PK', 2.79, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (21, 'Frikandeln', 6, 'PK', 3.49, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (22, 'Chips', 7, 'PK', 1.99, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (23, 'Salzstangen', 7, 'PK', 1.79, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (24, 'Gummibärchen', 7, 'PK', 1.59, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (25, 'Tee', 8, 'ST', 2.50, 0.19);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (26, 'Kaffee', 8, 'ST', 3.20, 0.19);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (27, 'Nudeln in Soße', 9, 'PK', 1.99, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (28, 'Ravioli', 9, 'PK', 1.89, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (29, 'Nudeln gebraten', 9, 'PK', 2.39, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (30, 'Reis süß/sauer', 9, 'PK', 2.19, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (31, 'Reisfladen', 10, 'ST', 2.00, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (32, 'Gedeckter Apflekuchen', 10, 'ST', 2.20, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (33, 'Belegtes Brötchen', 10, 'ST', 2.80, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (34, 'Graubrot', 10, 'ST', 1.90, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (35, 'Bild', 11, 'ST', 0.90, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (36, 'Kicker', 11, 'ST', 2.00, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (37, 'c''t', 11, 'ST', 3.70, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (38, 'Computerbild', 11, 'ST', 2.20, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (39, 'Zeit', 11, 'ST', 4.20, 0.07);
INSERT INTO mhist.produkt (id, bezeichnung, warengruppe_id, einheit, stueckpreis, umsatzsteuer) VALUES (43, 'GameStar', 11, 'ST', 6.50, 0.07);
