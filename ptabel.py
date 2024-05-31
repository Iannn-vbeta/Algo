class PTable:
    def __init__(self, headers):
        self.headers = headers
        self.rows = []
        self.column_widths = [len(header) for header in headers]
    
    def add_row(self, row):
        if len(row) != len(self.headers):
            raise ValueError("Row length does not match number of headers")
        self.rows.append(row)
        self.column_widths = [max(self.column_widths[i], len(str(row[i]))) for i in range(len(row))]
    
    def __str__(self):
        header_row = "| " + " | ".join([self.headers[i].ljust(self.column_widths[i]) for i in range(len(self.headers))]) + " |"
        separator_row = "+-" + "-+-".join(["-" * self.column_widths[i] for i in range(len(self.headers))]) + "-+"
        data_rows = "\n".join(["| " + " | ".join([str(row[i]).ljust(self.column_widths[i]) for i in range(len(row))]) + " |" for row in self.rows])
        
        return f"{separator_row}\n{header_row}\n{separator_row}\n{data_rows}\n{separator_row}"
    
    def print(self):
        print(self.__str__())

# Example usage:
SimpleTable = PTable
table = SimpleTable(["Name", "Age", "City"])
table.add_row(["Alice", 30, "New York"])
table.add_row(["Bob", 25, "San Francisco"])
table.add_row(["Charlie", 35, "Los Angeles"])

table.print()
