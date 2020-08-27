<#Comment here
Multiline comment#>

<#
$PSVersionTable
Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object -ExpandProperty Caption

$String = "This is my string"
$String.Length
$String.Split('i')
#>

$SwqlQuery = "SELECT TOP 5 NodeID, 
IPAddress, 
Caption,
CPUCount,
SystemUpTime,
DetailsUrl,
URI
FROM Orion.Nodes
WHERE Vendor = 'Cisco'
AND Status = 1
ORDER BY CPUCount DESC, SystemUpTime"

$SwisCreds = Get-Credential -Message "Enter your Orion creds"

$SwisConnection = Connect-Swis -Hostname "sunray.checkpoint.com" -Credential $SwisCreds

$Nodes = Get-SwisData -SwisConnection $SwisConnection -Query $SwqlQuery

ForEach ( $Node in $Nodes ) {
    $DaysUp = $Node.SystemUpTime / 60 / 60 / 24
    #Write-Host "Days up - $( $DaysUp )"
    if ( $DaysUp -lt 7 ) {
        Write-Host "Uptime of $( $Node.Caption ) is $( $DaysUp )"
    } else {
        Write-Host "This computer is up more than 7 days --> $( $Node.Caption )" -ForegroundColor Green
    }
}
