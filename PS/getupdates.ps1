param(
[string]$path
)

#Write-Host $path

$Session = New-Object -ComObject "Microsoft.Update.Session"
$Searcher = $Session.CreateUpdateSearcher()
$historyCount = $Searcher.GetTotalHistoryCount()

$Searcher.QueryHistory(0, $historyCount) | Select-Object Date,
    @{name="Operation"; expression={switch($_.operation){
    1 {"Installation"};}}}, 
            @{name="Status"; expression={switch($_.resultcode){
            2 {"Succeeded"}; 3 {"Succeeded With Errors"};}}}, Title, Description | Out-File -FilePath $path -Encoding ascii
