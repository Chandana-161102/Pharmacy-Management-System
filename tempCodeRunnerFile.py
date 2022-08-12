file = open(request.form['file'])
        csvreader = csv.reader(file)
        command="INSERT INTO "+table+" VALUES "
        for row in csvreader:
            command+="("
            for i in range(len(row)):
                if columname[i][1]!='int':
                    command+="'"+row[i]+"'"
                else:
                    command+=row[i]
                if i!=len(row)-1:
                    command+=","
            command+=")"
            command+=","
        fincommand = command[0:len(command)-1]
        print(fincommand)
        file.close()