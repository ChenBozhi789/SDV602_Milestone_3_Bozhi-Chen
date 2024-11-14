import data

current_file_path = 'local_data/nelson_weather.csv'
forecast_file_path = 'local_data/nelson_forecast_weather.csv'

current_result = data.read_local_data(current_file_path)
print(current_result)

forecast_result = data.read_local_data(forecast_file_path)
print(forecast_result)

# Template
{
    "tok":"9401b558-386d-48cb-ab8d-c2b418239ae7",
    "cmd":{
        "CREATE":"tbUser",
        "EXAMPLE":{"UserID PK":"TesterONE","Pwd":778899}
    }
}

# Jsn CREATE Table
{
    "CREATE": "tbUser",
    "EXAMPLE": {"UserID PK": "exampleUserID","Pwd": "examplePassword"}
}

# JsnDrop STORED 
{
    "STORE":"tbUser",
    "VALUE":[{"UserID":"Tesrer","Pwd":112233},{"UserID":"BozhiChen","Pwd":2000}]
}

# JsnDrop RETRIEVE
{
    "ALL":"tbUser"
} 

# JsnDrop SELECT
{
    "SELECT":"tbUser",
    "WHERE":"Pwd = 112233"
}

#JsnDrop UPDATE the record
{
    "STORE":"tblTest",
    "VALUE":[{"PersonID":"Todd","Score":3000}]
}

#JsnDrop DELETE the record
{
    "DELETE":"tbUser",
    "WHERE":"UserID= 'Tester'"
}

#JsnDrop DROP the table
{
    "DROP":"tbUser"
}