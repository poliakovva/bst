# HTML таблица, которая используется для создания PDF файла
html = """
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML  4.01//EN">
    <html>
     <head>
      <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
      <title>Тег TABLE</title>
     </head>
     <body>
      <table border="1" width="100%" cellpadding="5">
      <tr>
        <th>Материал / Услуга</th>
        <th>Стоимость</th>
       </tr>
       <tr>
        <th>Плитные материалы</th>
        <th>{p_row}</th>
       </tr>
       <tr>
        <th>Фурнитура стандарт</th>
        <th>{fs_row}</th>
       </tr>
       <tr>
        <th>Освещение</th>
        <th>{o_row}</th>
       </tr>
       <tr>
        <th>Фурнитура премиум</th>
        <th>{fp_row}</th>
       </tr>
       <tr>
        <th>Столярные изделия</th>
        <th>{s_row}</th>
       </tr>
       <tr>
        <th>Итоговая стоимость изделия</th>
        <th>{sum_row}</th>
       </tr>
       <tr>
        <th>Доставка</th>
        <th>{delivery_row} руб.</th>
       </tr>
       <tr>
        <th>Подъем на этаж на лифте</th>
        <th>{lifting_row} руб.</th>
       </tr>
       <tr>
        <th>Изготовление, сборка, монтаж</th>
        <th>{production_result} руб.</th>
       </tr>
       <tr>
        <th>Замер</th>
        <th>{measurement_row} руб.</th>
       </tr>
       <tr>
        <th>Проект</th>
        <th>{project_row} руб.</th>
       </tr>
       <tr>
        <th>Итоговая стоимость изделия и услуг</th>
        <th>{final_price_row}</th>
       </tr>
     </table>
     </body>
    </html>
"""
