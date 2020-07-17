[System.Reflection.Assembly]::LoadWithPartialName('Microsoft.VisualBasic') | Out-Null

Function Get-Folder($description="Please select a folder.", $initialDirectory="")
{
    [System.Reflection.Assembly]::LoadWithPartialName("System.windows.forms") | Out-Null
    $foldername = New-Object System.Windows.Forms.FolderBrowserDialog
    $foldername.Description = $description
    $foldername.rootfolder = "MyComputer"
    $foldername.SelectedPath = $initialDirectory
    if($foldername.ShowDialog() -eq "OK")
    {
        $folder += $foldername.SelectedPath
    }
    return $folder
}

$opponent_images = Get-Folder("Please select folder with opponent images.")
$participant_name =  [Microsoft.VisualBasic.Interaction]::InputBox("Please enter participant's name", "Participant name", "Participant")

python .\psap_core.py $participant_name $opponent_images