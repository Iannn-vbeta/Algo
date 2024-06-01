class PTable:
    def __init__(self, headers):
        self.headers = headers
        self.rows = []
        self.column_widths = [len(header) for header in headers]
        self.title = None

    def add_title(self, title):
        self.title = title

    def add_row(self, row):
        if len(row) != len(self.headers):
            raise ValueError("Jumlah kolom pada baris harus sama dengan jumlah kolom pada header")
        self.rows.append(row)
        self.column_widths = [max(self.column_widths[i], len(str(row[i]))) for i in range(len(row))]

    def __str__(self):
        header_row = "| " + " | ".join([self.headers[i].ljust(self.column_widths[i]) for i in range(len(self.headers))]) + " |"
        separator_row = "+-" + "-+-".join(["-" * self.column_widths[i] for i in range(len(self.headers))]) + "-+"
        data_rows = "\n".join(["| " + " | ".join([str(row[i]).ljust(self.column_widths[i]) for i in range(len(row))]) + " |" for row in self.rows])
        top_separator = "+" + "-" * (len(separator_row)-2) + "+"
        if self.title:
            title_row = self.title.center(len(separator_row)-2)
            return f"{top_separator}\n|{title_row}|\n{separator_row}\n{header_row}\n{separator_row}\n{data_rows}\n{separator_row}"
        else:
            return f"{separator_row}\n{header_row}\n{separator_row}\n{data_rows}\n{separator_row}"

    def print(self):
        print(self.__str__())

# contoh penggunaan
if __name__ == "__main__":
    table = PTable(["Nama", "Umur", "Kota"])
    table.add_title("Daftar Orang wdawafgaw awdrfwaf")
    table.add_row(["Fana", 30000, "Dewa"])
    table.add_row(["MasFana", 25000, "Eden"])
    table.add_row(["Ilak", 35, "Bowait"])

    table.print()
