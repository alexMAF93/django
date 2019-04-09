def sort_data(string):
    data = string.split(';')
    output_data = []
    i = 0
    while i < len(data) - 1:
        output_data.append({
                            'Manga': data[i + 0],
                            'Chapter': data[i + 1],
                            'Released_date': data[i + 2],
        })
        i += 3
    return output_data
