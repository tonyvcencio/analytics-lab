Attribute VB_Name = "Module1"

Option Explicit

Public Sub ImportDailyExports()

    Dim projectPath As String
    Dim sourceFolder As String

    projectPath = ThisWorkbook.Path
    sourceFolder = Replace(projectPath, "\excel", "\data\daily-exports")


If Dir(sourceFolder & "\External_Open.csv") = "" Then
    Err.Raise vbObjectError + 1001, _
              "ImportDailyExports", _
              "External CSV file not found."
End If

If Dir(sourceFolder & "\Internal_Open.csv") = "" Then
    Err.Raise vbObjectError + 1002, _
              "ImportDailyExports", _
              "Internal CSV file not found."
End If

    ImportCSV sourceFolder & "\External_Open.csv", _
              ThisWorkbook.Worksheets("External_Data")

    ImportCSV sourceFolder & "\Internal_Open.csv", _
              ThisWorkbook.Worksheets("Internal_Data")

    MsgBox "Daily exports imported successfully." & vbCrLf & _
           "External records: " & _
           ThisWorkbook.Worksheets("External_Data").Cells( _
           Rows.Count, 1).End(xlUp).Row - 1 & vbCrLf & _
           "Internal records: " & _
           ThisWorkbook.Worksheets("Internal_Data").Cells( _
           Rows.Count, 1).End(xlUp).Row - 1, vbInformation

End Sub

Private Sub ImportCSV(ByVal filePath As String, ByVal targetSheet As Worksheet)

    Dim sourceBook As Workbook

    targetSheet.Cells.Clear

    Set sourceBook = Workbooks.Open(Filename:=filePath, Local:=True)

    sourceBook.Worksheets(1).UsedRange.Copy _
        Destination:=targetSheet.Range("A1")

    sourceBook.Close SaveChanges:=False

    targetSheet.Columns.AutoFit

End Sub



Public Sub ReconcileWorkOrders()

    Dim wsExternal As Worksheet
    Dim wsInternal As Worksheet
    Dim wsAging As Worksheet

    Dim lastExternal As Long
    Dim lastInternal As Long
    Dim outputRow As Long
    Dim i As Long

    Dim workOrderID As String
    Dim matchCount As Long

    Set wsExternal = ThisWorkbook.Worksheets("External_Data")
    Set wsInternal = ThisWorkbook.Worksheets("Internal_Data")
    Set wsAging = ThisWorkbook.Worksheets("Aging_Detail")

    wsAging.Cells.Clear

    wsAging.Range("A1:D1").Value = Array( _
        "WorkOrderID", "ExternalOpen", "InternalOpen", "Classification")

    lastExternal = wsExternal.Cells(wsExternal.Rows.Count, 1).End(xlUp).Row
    lastInternal = wsInternal.Cells(wsInternal.Rows.Count, 1).End(xlUp).Row

    outputRow = 2

    ' First pass: every external work order
    For i = 2 To lastExternal

        workOrderID = Trim(CStr(wsExternal.Cells(i, 1).Value))

        If Len(workOrderID) > 0 Then

            matchCount = Application.WorksheetFunction.CountIf( _
                wsInternal.Range("A2:A" & lastInternal), workOrderID)

            wsAging.Cells(outputRow, 1).Value = workOrderID
            wsAging.Cells(outputRow, 2).Value = "Yes"

            If matchCount > 0 Then
                wsAging.Cells(outputRow, 3).Value = "Yes"
                wsAging.Cells(outputRow, 4).Value = "Matched"
            Else
                wsAging.Cells(outputRow, 3).Value = "No"
                wsAging.Cells(outputRow, 4).Value = "External Only"
            End If

            outputRow = outputRow + 1

        End If

    Next i

    ' Second pass: internal records absent from external
    For i = 2 To lastInternal

        workOrderID = Trim(CStr(wsInternal.Cells(i, 1).Value))

        If Len(workOrderID) > 0 Then

            matchCount = Application.WorksheetFunction.CountIf( _
                wsExternal.Range("A2:A" & lastExternal), workOrderID)

            If matchCount = 0 Then

                wsAging.Cells(outputRow, 1).Value = workOrderID
                wsAging.Cells(outputRow, 2).Value = "No"
                wsAging.Cells(outputRow, 3).Value = "Yes"
                wsAging.Cells(outputRow, 4).Value = "Internal Only"

                outputRow = outputRow + 1

            End If

        End If

    Next i

    wsAging.Columns("A:D").AutoFit

    MsgBox "Reconciliation complete." & vbCrLf & _
           "Unique active work orders: " & outputRow - 2, vbInformation

End Sub



Public Sub CalculateAging()

    Dim wsAging As Worksheet
    Dim wsExternal As Worksheet
    Dim wsInternal As Worksheet

    Dim lastRow As Long
    Dim lastExternal As Long
    Dim lastInternal As Long
    Dim i As Long
    Dim matchRow As Variant

    Dim workOrderID As String
    Dim createdDate As Variant
    Dim dueDate As Variant
    Dim ageDays As Long
    Dim reportDate As Date

    Set wsAging = ThisWorkbook.Worksheets("Aging_Detail")
    Set wsExternal = ThisWorkbook.Worksheets("External_Data")
    Set wsInternal = ThisWorkbook.Worksheets("Internal_Data")

    reportDate = DateSerial(2026, 10, 31)

    lastRow = wsAging.Cells(wsAging.Rows.Count, 1).End(xlUp).Row
    lastExternal = wsExternal.Cells(wsExternal.Rows.Count, 1).End(xlUp).Row
    lastInternal = wsInternal.Cells(wsInternal.Rows.Count, 1).End(xlUp).Row

    wsAging.Range("E1:I1").Value = Array( _
        "CreatedDate", "AgeDays", "AgingBucket", _
        "DueDate", "Overdue")

    For i = 2 To lastRow

        workOrderID = Trim(CStr(wsAging.Cells(i, 1).Value))

        ' Prefer external source when available.
        matchRow = Application.Match( _
            workOrderID, wsExternal.Range("A2:A" & lastExternal), 0)

        If Not IsError(matchRow) Then

            createdDate = wsExternal.Cells(matchRow + 1, 2).Value
            dueDate = wsExternal.Cells(matchRow + 1, 6).Value

        Else

            ' Internal-only records use the internal export.
            matchRow = Application.Match( _
                workOrderID, wsInternal.Range("A2:A" & lastInternal), 0)

            If Not IsError(matchRow) Then
                createdDate = wsInternal.Cells(matchRow + 1, 2).Value
                dueDate = wsInternal.Cells(matchRow + 1, 5).Value
            Else
                GoTo NextRecord
            End If

        End If

        If IsDate(createdDate) Then

            wsAging.Cells(i, 5).Value = CDate(createdDate)

            ageDays = DateDiff("d", CDate(createdDate), reportDate)

            wsAging.Cells(i, 6).Value = ageDays

            Select Case ageDays
                Case 0 To 2
                    wsAging.Cells(i, 7).Value = "Fresh"
                Case 3 To 5
                    wsAging.Cells(i, 7).Value = "Developing"
                Case 6 To 10
                    wsAging.Cells(i, 7).Value = "Aging"
                Case 11 To 20
                    wsAging.Cells(i, 7).Value = "High Aging"
                Case Is >= 21
                    wsAging.Cells(i, 7).Value = "Critical Aging"
                Case Else
                    wsAging.Cells(i, 7).Value = "Invalid Date"
            End Select

        Else
            wsAging.Cells(i, 7).Value = "Missing Date"
        End If

        If IsDate(dueDate) Then

            wsAging.Cells(i, 8).Value = CDate(dueDate)

            If CDate(dueDate) < reportDate Then
                wsAging.Cells(i, 9).Value = "Yes"
            Else
                wsAging.Cells(i, 9).Value = "No"
            End If

        Else
            wsAging.Cells(i, 9).Value = "Missing Due Date"
        End If

NextRecord:
    Next i

    wsAging.Columns("E").NumberFormat = "mm/dd/yyyy"
    wsAging.Columns("H").NumberFormat = "mm/dd/yyyy"
    wsAging.Columns("A:I").AutoFit

    MsgBox "Aging calculations complete.", vbInformation

End Sub



Public Sub GenerateExceptions()

    Dim wsAging As Worksheet
    Dim wsExceptions As Worksheet
    Dim lastRow As Long
    Dim outputRow As Long
    Dim i As Long
    Dim classification As String

    Set wsAging = ThisWorkbook.Worksheets("Aging_Detail")
    Set wsExceptions = ThisWorkbook.Worksheets("Exceptions")

    wsExceptions.Cells.Clear

    wsExceptions.Range("A1:G1").Value = Array( _
        "WorkOrderID", "Classification", "CreatedDate", _
        "AgeDays", "DueDate", "Overdue", "ReviewStatus")

    lastRow = wsAging.Cells(wsAging.Rows.Count, 1).End(xlUp).Row
    outputRow = 2

    For i = 2 To lastRow

        classification = Trim(CStr(wsAging.Cells(i, 4).Value))

        If classification = "External Only" Or _
           classification = "Internal Only" Then

            wsExceptions.Cells(outputRow, 1).Value = _
                wsAging.Cells(i, 1).Value

            wsExceptions.Cells(outputRow, 2).Value = classification

            wsExceptions.Cells(outputRow, 3).Value = _
                wsAging.Cells(i, 5).Value

            wsExceptions.Cells(outputRow, 4).Value = _
                wsAging.Cells(i, 6).Value

            wsExceptions.Cells(outputRow, 5).Value = _
                wsAging.Cells(i, 8).Value

            wsExceptions.Cells(outputRow, 6).Value = _
                wsAging.Cells(i, 9).Value

            wsExceptions.Cells(outputRow, 7).Value = _
                "Pending Review"

            outputRow = outputRow + 1

        End If

    Next i

    wsExceptions.Columns("C").NumberFormat = "mm/dd/yyyy"
    wsExceptions.Columns("E").NumberFormat = "mm/dd/yyyy"
    wsExceptions.Columns("A:G").AutoFit

    MsgBox "Exceptions report generated." & vbCrLf & _
           "Source discrepancies: " & outputRow - 2, vbInformation

End Sub



Public Sub GenerateSummary()

    Dim wsSummary As Worksheet
    Dim wsAging As Worksheet
    Dim wsExceptions As Worksheet
    Dim lastRow As Long
    Dim totalActive As Long
    Dim totalMatched As Long
    Dim externalOnly As Long
    Dim internalOnly As Long
    Dim totalOverdue As Long
    Dim criticalAging As Long
    Dim bucketNames As Variant
    Dim i As Long

    Set wsSummary = ThisWorkbook.Worksheets("Summary")
    Set wsAging = ThisWorkbook.Worksheets("Aging_Detail")
    Set wsExceptions = ThisWorkbook.Worksheets("Exceptions")

    lastRow = wsAging.Cells(wsAging.Rows.Count, "A").End(xlUp).Row

    If lastRow < 2 Then
        MsgBox "No aging data available. Run reconciliation first.", _
               vbExclamation
        Exit Sub
    End If

    totalActive = lastRow - 1

    totalMatched = Application.CountIf( _
        wsAging.Range("D2:D" & lastRow), "Matched")

    externalOnly = Application.CountIf( _
        wsAging.Range("D2:D" & lastRow), "External Only")

    internalOnly = Application.CountIf( _
        wsAging.Range("D2:D" & lastRow), "Internal Only")

    totalOverdue = Application.CountIf( _
        wsAging.Range("I2:I" & lastRow), "Yes")

    criticalAging = Application.CountIf( _
        wsAging.Range("G2:G" & lastRow), "Critical Aging")

    wsSummary.Cells.Clear

    ' Dashboard heading
    With wsSummary.Range("B2:H2")
        .Merge
        .Value = "MERIDIAN PROPERTY SERVICES"
        .Font.Size = 20
        .Font.Bold = True
    End With

    wsSummary.Range("B3").Value = "DAILY OPERATIONS SUMMARY"
    wsSummary.Range("B4").Value = "Report Date"
    wsSummary.Range("C4").Value = DateSerial(2026, 10, 31)
    wsSummary.Range("C4").NumberFormat = "mmmm d, yyyy"

    ' KPI labels and values
    wsSummary.Range("B6").Value = "ACTIVE BACKLOG"
    wsSummary.Range("C6").Value = totalActive

    wsSummary.Range("B7").Value = "MATCHED RECORDS"
    wsSummary.Range("C7").Value = totalMatched

    wsSummary.Range("B8").Value = "SOURCE DISCREPANCIES"
    wsSummary.Range("C8").Value = externalOnly + internalOnly

    wsSummary.Range("B9").Value = "EXTERNAL ONLY"
    wsSummary.Range("C9").Value = externalOnly

    wsSummary.Range("B10").Value = "INTERNAL ONLY"
    wsSummary.Range("C10").Value = internalOnly

    wsSummary.Range("B11").Value = "OVERDUE WORK ORDERS"
    wsSummary.Range("C11").Value = totalOverdue

    wsSummary.Range("B12").Value = "CRITICAL AGING"
    wsSummary.Range("C12").Value = criticalAging

    ' Aging distribution
    wsSummary.Range("E6").Value = "AGING CATEGORY"
    wsSummary.Range("F6").Value = "WORK ORDERS"

    bucketNames = Array( _
        "Fresh", "Developing", "Aging", _
        "High Aging", "Critical Aging")

    For i = 0 To 4
        wsSummary.Cells(i + 7, 5).Value = bucketNames(i)
        wsSummary.Cells(i + 7, 6).Value = _
            Application.CountIf( _
                wsAging.Range("G2:G" & lastRow), bucketNames(i))
    Next i

    ' Format KPI section
    With wsSummary.Range("B6:C12")
        .Borders.LineStyle = xlContinuous
        .Borders.Color = RGB(220, 225, 230)
    End With

    wsSummary.Range("B6:B12").Font.Bold = True
    wsSummary.Range("C6:C12").Font.Bold = True
    wsSummary.Range("C6:C12").Font.Size = 14

    wsSummary.Range("B6:C6").Interior.Color = RGB(220, 235, 245)
    wsSummary.Range("B8:C8").Interior.Color = RGB(255, 235, 205)
    wsSummary.Range("B11:C12").Interior.Color = RGB(255, 225, 225)

    ' Format aging table
    With wsSummary.Range("E6:F6")
        .Font.Bold = True
        .Interior.Color = RGB(40, 55, 75)
        .Font.Color = RGB(255, 255, 255)
    End With

    wsSummary.Range("E6:F11").Borders.LineStyle = xlContinuous

    wsSummary.Columns("A").ColumnWidth = 3
    wsSummary.Columns("B").ColumnWidth = 28
    wsSummary.Columns("C").ColumnWidth = 18
    wsSummary.Columns("D").ColumnWidth = 4
    wsSummary.Columns("E").ColumnWidth = 22
    wsSummary.Columns("F").ColumnWidth = 18

    ' Create aging chart
    Dim chartObject As chartObject

    For Each chartObject In wsSummary.ChartObjects
        chartObject.Delete
    Next chartObject

    Set chartObject = wsSummary.ChartObjects.Add( _
        Left:=wsSummary.Range("E14").Left, _
        Top:=wsSummary.Range("E14").Top, _
        Width:=460, Height:=260)

    With chartObject.Chart
        .ChartType = xlColumnClustered
        .SetSourceData Source:=wsSummary.Range("E6:F11")
        .HasTitle = True
        .ChartTitle.Text = "Active Backlog by Aging Category"
        .HasLegend = False
    End With

    wsSummary.Activate
    wsSummary.Range("B2").Select

    MsgBox "Daily operations summary generated.", vbInformation

End Sub



Public Sub RunDailyReport()

    Dim startTime As Double
    Dim elapsedSeconds As Double

    startTime = Timer

    Application.ScreenUpdating = False

    On Error GoTo ReportError

    ' Step 1: Import both daily CSV exports
    ImportDailyExports

    ' Step 2: Reconcile active work orders
    ReconcileWorkOrders

    ' Step 3: Calculate aging and overdue status
    CalculateAging

    ' Step 4: Identify source discrepancies
    GenerateExceptions

    ' Step 5: Build the management dashboard
    GenerateSummary

    elapsedSeconds = Timer - startTime

    Application.ScreenUpdating = True

    MsgBox "Daily reporting workflow completed." & vbCrLf & _
           "Processing time: " & _
           Format(elapsedSeconds, "0.00") & " seconds", _
           vbInformation, "Meridian Aging Monitor"

    Exit Sub

ReportError:

    Application.ScreenUpdating = True

    MsgBox "Reporting workflow failed:" & vbCrLf & _
           Err.Description, vbCritical, "Meridian Aging Monitor"

End Sub


