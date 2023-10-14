# Define the folder path where the files are located
$folderPath = "C:\Users\godfrey\Desktop\AI Music Training\ARCHIVEDOLDBEATS"

# Iterate through each file in the folder
Get-ChildItem -Path $folderPath | ForEach-Object {
    # Get the original file name
    $originalName = $_.Name

    # Remove all spaces
    $newName = $originalName -replace ' ', ''

    # Replace dashes with underscores
    $newName = $newName -replace '-', '_'

    # Remove special characters (anything that's not a number, letter, underscore or dot)
    $newName = $newName -replace '[^\w\.]', ''

    # Rename the file
    if ($newName -ne $originalName) {
        Rename-Item -Path $_.FullName -NewName $newName
        Write-Host ("Renamed {0} to {1}" -f $originalName, $newName)
    }
}