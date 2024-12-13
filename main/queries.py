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
    m.nomi as tur_nomi,
 	m2.nomi AS maxsulot_nomi,
 	m2.MARKA AS marka,
 	m2.MODEL AS model,
 	c.MIQDOR AS miqdor,
 	k.usd AS usd,
 	sum(c.MIQDOR*k.USD) AS summa,
 	k.YVAQT AS kirim_sana,
 	c.YVAQT AS chiqim_vaqt
FROM 
 	CHIQIM c
LEFT JOIN 
 	MAXSULOT m2 on m2.id=c.MAXSULOT_ID 
LEFT JOIN 
 	MAXSULOTTUR m ON m.id=m2.TUR_ID 
LEFT JOIN
	KIRIM k ON k.id=c.KIRIM_ID 
WHERE 
	c.YVAQT BETWEEN ? AND ? AND m.id=?
GROUP BY
	c.id,m.id,m.nomi,m2.nomi,m2.marka,m2.model,c.MIQDOR,k.usd,k.YVAQT, c.YVAQT"""