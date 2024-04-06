```
FUNCTION find_links():
    url = 'https://www.statistics.gr/el/statistics/-/publication/STO04/'
    r = REQUESTS.GET(url)
    html_content = r.text
    soup = PARSE_HTML(html_content)

    history_wrapper = soup.FIND('div', {'class': 'history-wrapper'})
    links = []

    FOR a IN history_wrapper.FIND_ALL('a'):
        name = a.FIND('div').text
        IF MATCH('^4.*201[1-5]$', name):
            link = urljoin(url, a['href'])
            links.APPEND((name[-4:], link))

    RETURN links


FUNCTION download_files(links, save_dir = 'xls_files/'):
    FOR name, url IN links:
        r = REQUESTS.GET(url)
        html_content = r.text
        soup = PARSE_HTML(html_content)

        a = soup.FIND('a', string=MATCH('Αφίξεις μη κατοίκων από το εξωτερικό ανά χώρα προέλευσης και μέσο μεταφοράς'))

        resp = REQUESTS.GET(a['href'])

        CREATE_DIRECTORY(os.path.dirname(save_dir), exist_ok=True)
        output = OPEN(os.path.join(save_dir, name + '.xls'), 'wb')
        output.WRITE(resp.content)
        output.CLOSE()
        
        PRINT('Year {} dataset was successfully downloaded!'.FORMAT(name))


FUNCTION download_set():
    links = find_links()
    download_files(links)


FUNCTION save_to_db_and_csv(xls_dir = 'xls_files/', csv_dir = 'csv_files/', sql_dir = '', sql_name = 'db'):
    CREATE_DIRECTORY(os.path.dirname(csv_dir), exist_ok=True)
    db = CONNECT_TO_SQLITE(os.path.join(sql_dir, sql_name + '.sqlite'))

    FOR name IN ['2011', '2012', '2013', '2014', '2015']:
        dfs = READ_EXCEL(os.path.join(xls_dir, name + '.xls'), sheet_name=None)

        FOR table, df IN dfs.items():
            df.COLUMNS = ['id', 'ΧΩΡΑ', 'ΑΕΡΟΠΟΡΙΚΩΣ', 'ΣΙΔ/ΚΩΣ', 'ΘΑΛΑΣΣΙΩΣ', 'ΟΔΙΚΩΣ', 'ΣΥΝΟΛΟ']
            df = df[FILTER(df.id.str.CONTAINS('^\d+\.$', na=False))]
            df = df.DROP('id', 1)
            df = df.FILLNA(0)
            df['ΧΩΡΑ'] = df['ΧΩΡΑ'].REPLACE('\s$', '', regex=True)
            df['ΧΩΡΑ'] = df['ΧΩΡΑ'].REPLACE(' \(\d+\)$', '', regex=True)
            df = df.DROP_DUPLICATES(subset=['ΧΩΡΑ'], keep='first')

            FOR collumn IN ['ΑΕΡΟΠΟΡΙΚΩΣ', 'ΣΙΔ/ΚΩΣ', 'ΘΑΛΑΣΣΙΩΣ', 'ΟΔΙΚΩΣ', 'ΣΥΝΟΛΟ']:
                df[collumn] = df[collumn].ROUND()
                df[collumn] = df[collumn].ASTYPE(INT)

            df.TO_SQL(name + '-' + month_to_id[table], db, if_exists='replace', index=False)
            df.TO_CSV(os.path.join(csv_dir, name + '-' + month_to_id[table] + '.csv'), index=False)
    
    PRINT('Data are now in a safe place!')


FUNCTION get_dataframes_dict(csv_dir = 'csv_files/'):
    directory = LIST_FILES(csv_dir)
    dfs = {}

    FOR file IN SORT(directory):
        filename = DECODE(file)
        year_month = SUB(filename, '\.csv$', '')
        year, month = SPLIT(year_month, '-')
        filepath = JOIN(csv_dir, filename)
        df = READ_CSV(filepath)

        year = PARSE_INT(year)
        month = PARSE_INT(month)

        IF year NOT IN dfs:
            dfs[year] = {}
        dfs[year][month] = df

    RETURN dfs


FUNCTION per_year(dfs, charts_dir='charts/', picture_name='per_year'):
    years = []

    FOR year, months IN dfs.items():
        df = CONCAT([months[month] FOR month IN RANGE(1,13)], ignore_index=True)
        df = df.SUM()
        years.APPEND((year, df['ΣΥΝΟΛΟ']))

    x, y = UNZIP(years)
    
    PLOT_BAR(x, y)
    SAVE_PLOT(JOIN(charts_dir, picture_name), bbox_inches='tight', dpi=100)
    SHOW_PLOT()


FUNCTION per_quarter(dfs, charts_dir='charts/', picture_name='per_quarter'):
    quarters = []

    FOR year, months IN dfs.items():
        FOR quarter IN RANGE(1,5):
            df = CONCAT([months[month] FOR month IN RANGE(3*quarter - 2, 3*quarter + 1)], ignore_index=True)
            df = df.SUM()
            quarters.APPEND(('{}-Q{}'.FORMAT(year, quarter), df['ΣΥΝΟΛΟ']))

    x, y = UNZIP(quarters)
    
    PLOT_BAR(x, y)
    SAVE_PLOT(JOIN(charts_dir, picture_name), bbox_inches='tight', dpi=100)
    SHOW_PLOT()


FUNCTION per_transport(dfs, charts_dir='charts/', picture_name='per_transport'):
    df = CONCAT(dfs, ignore_index=True)
    df = df.DROP('ΧΩΡΑ', 1)
    df = df.DROP('ΣΥΝΟΛΟ', 1)
    df = df.SUM()

    PLOT_BAR(df)
    SET_YSCALE('log')
    SAVE_PLOT(JOIN(charts_dir, picture_name), bbox_inches='tight', dpi=100)
    SHOW_PLOT()


FUNCTION per_country(dfs, top_n=10, charts_dir='charts/', picture_name='per_country'):
    df = CONCAT(dfs, ignore_index=True)
    df = df.GROUP_BY(['ΧΩΡΑ'], as_index=False)[['ΑΕΡΟΠΟΡΙΚΩΣ', 'ΣΙΔ/ΚΩΣ', 'ΘΑΛΑΣΣΙΩΣ', 'ΟΔΙΚΩΣ', 'ΣΥΝΟΛΟ']].SUM()
    df = df.SORT('ΣΥΝΟΛΟ', ascending=False).HEAD(10)

    x = df['ΧΩΡΑ']
    y = df['ΣΥΝΟΛΟ']

    PLOT_BAR(x, y)
    SAVE_PLOT(JOIN(charts_dir, picture_name), bbox_inches='tight', dpi=100)
    SHOW_PLOT()


FUNCTION paint_set(option='year'):
    dfs_dict = get_dataframes_dict()
    plain_dfs = [month_df FOR months_dict IN dfs_dict.values() FOR month_df IN LIST(months_dict.values())]

    IF option == 'year':
        per_year(dfs_dict)
    ELSE IF option == 'country':
        per_country(plain_dfs)
    ELSE IF option == 'transport':
        per_transport(plain_dfs)
    ELSE:
        per_quarter(dfs_dict)

    PRINT('Plot was successful!')


FUNCTION main():
    parent = CREATE_WINDOW()
    parent.TITLE('!The Ultimate Program of the Universe!')

    button_frame = CREATE_FRAME(parent, bd=20)
    button_frame.PACK()

    text_frame = CREATE_FRAME(parent, bd=20)
    text_frame.PACK(side=BOTTOM)

    download_btn = CREATE_BUTTON(button_frame, text='DOWNLOAD', command=download_set, height=5, width=20, bg='#c7cace')
    download_btn.PACK(side=LEFT)

    store_btn = CREATE_BUTTON(button_frame, text='STORE', command=store_set, height=5, width=20, bg='#a7cace', state='disabled')
    store_btn.PACK(side=LEFT)

    paint_year_btn = CREATE_BUTTON(button_frame, text='PAINT per year', command=lambda: paint_set(option='year'), height=5, width=20, bg='#97cace', state='disabled')
    paint_year_btn.PACK(side=LEFT)

    paint_country_btn = CREATE_BUTTON(button_frame, text='PAINT per country', command=lambda: paint_set(option='country'), height=5, width=20, bg='#97cace', state='disabled')
    paint_country_btn.PACK(side=LEFT)

    paint_transport_btn = CREATE_BUTTON(button_frame, text='PAINT per transport', command=lambda: paint_set(option='transport'), height=5, width=20, bg='#97cace', state='disabled')
    paint_transport_btn.PACK(side=LEFT)

    paint_quarter_btn = CREATE_BUTTON(button_frame, text='PAINT per quarter', command=lambda: paint_set(option='quarter'), height=5, width=20, bg='#97cace', state='disabled')
    paint_quarter_btn.PACK(side=LEFT)

    label = CREATE_LABEL(text_frame, text="Hello!")
    label.PACK()

    parent.MAINLOOP()

IF __NAME__ == '__MAIN__':
    main()
```