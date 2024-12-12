# types = """SELECT id,NOMI FROM MAXSULOTTUR m """

types = """SELECT 
    m.id as tur_id,
    m.NOMI AS tur,
    sum(c.miqdor) AS miqdor,
    SUM(c.MIQDOR * k.USD) AS jami_summa
FROM 
    CHIQIM c
LEFT JOIN 
    MAXSULOT m2 ON m2.id = c.MAXSULOT_ID 
LEFT JOIN 
    MAXSULOTTUR m ON m.id = m2.TUR_ID 
LEFT JOIN 
	kirim k ON k.id=c.KIRIM_ID 
WHERE 
    c.YVAQT BETWEEN ? AND ?
GROUP BY
    m.id,m.NOMI"""

product = """SELECT 
	m.id AS tur_id,
 	m.NOMI AS tur,
 	m2.nomi AS maxsulot_nomi,
 	m2.MARKA AS marka,
 	m2.MODEL AS model,
 	c.MIQDOR AS miqdor,
 	c.snarx,
 	k.usd AS usd,
 	sum(c.MIQDOR*k.USD) AS summa,
 	c.YVAQT AS y_vaqt
FROM 
 	CHIQIM c
LEFT JOIN 
 	MAXSULOT m2 on m2.id=c.MAXSULOT_ID 
LEFT JOIN 
 	MAXSULOTTUR m ON m.id=m2.TUR_ID 
LEFT JOIN
	KIRIM k ON k.id=c.KIRIM_ID 
WHERE 
	m.nomi != '1' AND c.YVAQT BETWEEN '2024-12-01' AND '2024-12-31' AND m.id=98
GROUP BY
	m.id,m.nomi,m2.nomi,c.MIQDOR,k.usd,c.YVAQT,c.snarx,m2.marka,m2.model"""