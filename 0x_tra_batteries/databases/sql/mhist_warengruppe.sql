create table warengruppe
(
    id          int auto_increment
        primary key,
    bezeichnung varchar(100) null
)
    charset = utf8;

INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (1, 'TK');
INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (2, 'Obst, Gemüse');
INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (3, 'Wurst, Aufschnitt');
INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (4, 'Milchprodukte');
INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (5, 'Kaltgetränke');
INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (6, 'Grillgut');
INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (7, 'Snacks, Süsswaren');
INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (8, 'Heissgetränke');
INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (9, 'Fertiggerichte');
INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (10, 'Brot, Backwaren');
INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (11, 'Zeitschriften');
INSERT INTO mhist.warengruppe (id, bezeichnung) VALUES (12, 'Dienstleistung');
