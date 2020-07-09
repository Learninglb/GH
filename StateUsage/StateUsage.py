Imports System.Data.OracleClient



    Private Sub Form1_Load(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles MyBase.Load
        ' Stop
        Button2.Visible = False
        Period = Now.AddDays(-7).ToString("yyyyMM")
        TextBox1.Text = Period
        ocn = FECUtil.Database.getOracleConnection("cis")
        Try
            ocn.Open()
        Catch ex As Exception
            MessageBox.Show(ex.ToString)
        End Try
    End Sub

    Private Sub Button1_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button1.Click
        If TextBox1.Text.Trim.Length <> 6 Then
            MessageBox.Show("Invalid Period...")
            Exit Sub
        End If
        BillCycle = TextBox1.Text.Substring(4, 2) & TextBox1.Text.Substring(0, 4)
        Dim sp(2) As Char
        sp = vbCrLf.ToCharArray
        Dim Account As String
        Dim Accts(0) As String
        Account = My.Computer.FileSystem.ReadAllText("StateUsageQuery.Txt")
        Accts = Account.Split(vbCrLf.ToCharArray, System.StringSplitOptions.RemoveEmptyEntries)
        '  Accts(0) = "1007077"
        Period = TextBox1.Text.Trim
        Dim cmdString As String = String.Empty
        cmd = New OracleCommand("", ocn)
        dt = New DataTable("StateUsage")

        Dim col As New DataColumn("Account")
        dt.Columns.Add(col)
        col = New DataColumn("Name")
        dt.Columns.Add(col)
        col = New DataColumn("Srv_Loc_Nbr")
        dt.Columns.Add(col)
        col = New DataColumn("Meter")
        dt.Columns.Add(col)
        col = New DataColumn("Cycle_Start")
        dt.Columns.Add(col)
        col = New DataColumn("Cycle_End")
        dt.Columns.Add(col)
        col = New DataColumn("KWH")
        dt.Columns.Add(col)
        col = New DataColumn("KW")
        dt.Columns.Add(col)
        col = New DataColumn("Consumption_Charge", Type.GetType("System.Decimal"))
        dt.Columns.Add(col)
        col = New DataColumn("Basic_Charge", Type.GetType("System.Decimal"))
        dt.Columns.Add(col)
        col = New DataColumn("Total_Charge", Type.GetType("System.Decimal"))
        dt.Columns.Add(col)
        col = New DataColumn("SrvAddr1")
        dt.Columns.Add(col)
        col = New DataColumn("SrvAddr2")
        dt.Columns.Add(col)
        col = New DataColumn("SrvDesc")
        dt.Columns.Add(col)
        col = New DataColumn("City")
        dt.Columns.Add(col)
        col = New DataColumn("Zip")
        dt.Columns.Add(col)
        Dim dr As DataRow = Nothing
        Dim srvLoc As Double = 0

        For Each Account In Accts
            srvLoc = 0  '  Re-Initialize for each account
            cmdString = "SELECT  BI_ACCT, BI_SRV_LOC_NBR, BI_MTR_NBR, BI_USAGE, TO_CHAR(BI_PREV_READ_DT + 1, 'yyyymmdd') AS BEGINCYCLE, " _
                      & "TO_CHAR(BI_PRES_READ_DT,'yyyymmdd') AS ENDCYCLE, BI_ACTUAL_DMD_USAGE " _
                      & "FROM(CIS28013.BI_HIST_USAGE) " _
                      & "WHERE (BI_ACCT = " & Account.Trim & ") AND (BI_REV_YRMO = " & Period & ") ORDER BY BI_SRV_LOC_NBR"
            cmd.CommandText = cmdString
            rdr = cmd.ExecuteReader
            If rdr.HasRows Then
                While rdr.Read()
                    If rdr("BI_SRV_LOC_NBR") <> srvLoc Then
                        If srvLoc <> 0 AndAlso srvLoc <> rdr("BI_SRV_LOC_NBR") Then   ' Store datarow for 1st...  SrvLocs  - If it = 0 then there is no datarow to add to the table
                            dt.Rows.Add(dr)
                        End If
                        srvLoc = rdr("BI_SRV_LOC_NBR")
                        dr = dt.NewRow
                        dr("KWH") = 0
                        dr("Cycle_End") = String.Empty
                        dr("Cycle_Start") = String.Empty
                    End If

                    dr("Account") = rdr("BI_ACCT")
                    dr("Srv_Loc_Nbr") = rdr("BI_SRV_LOC_NBR")
                    dr("Meter") = rdr("BI_MTR_NBR")
                    dr("KWH") += rdr("BI_USAGE")
                    If dr("Cycle_Start") > rdr("BEGINCYCLE") Or dr("Cycle_Start") = String.Empty Then  '  Account for meter changes
                        dr("Cycle_Start") = rdr("BEGINCYCLE")
                    End If
                    If dr("Cycle_End") < rdr("ENDCYCLE") Then
                        dr("Cycle_End") = rdr("ENDCYCLE")
                    End If
                    dr("KW") = rdr("BI_ACTUAL_DMD_USAGE")
                End While
                dt.Rows.Add(dr)   '  Get the last row for this account/srvloc 
            Else
                rdr.Close()
                Continue For
            End If
            rdr.Close()
        Next

        If dt.Rows.Count > 0 Then
            For Each dr In dt.Rows
                dr("Basic_Charge") = 0D
                dr("Consumption_Charge") = 0D
                cmdString = "SELECT BI_CHG_CD, BI_CHG_AMT " _
                          & "FROM(CIS28013.BI_HIST_CHG) " _
                          & "WHERE (BI_ACCT = " & dr("Account") & ") AND (BI_REV_YRMO = " & Period & ") " _
                          & "AND (BI_SRV_LOC_NBR = " & dr("Srv_Loc_Nbr") & ") AND (BI_BC_CD = 'B')"
                cmd.CommandText = cmdString
                rdr = cmd.ExecuteReader
                Dim total As Decimal = 0D
                While rdr.Read
                    total += Convert.ToDecimal(rdr("BI_CHG_AMT"))
                    If rdr("BI_CHG_CD") = 91 Then
                        dr("Basic_Charge") = rdr("BI_CHG_AMT")
                    ElseIf rdr("BI_CHG_CD") = 71 Then
                        dr("Consumption_Charge") = rdr("BI_CHG_AMT")
                    Else
                    End If
                End While
                rdr.Close()
                dr("Total_Charge") = total
            Next

            For Each dr In dt.Rows

                cmdString = "Select BI_FORMAT_NAME " _
                          & "FROM(CIS28013.BI_CONSUMER_VIEW_1) " _
                          & "WHERE(BI_VWN_CO_ACCT = " & dr("Account") & ")"
                cmd.CommandText = cmdString
                rdr = cmd.ExecuteReader
                While rdr.Read
                    If rdr.HasRows Then
                        dr("Name") = rdr(0)
                    End If
                End While
                rdr.Close()
            Next

            For Each dr In dt.Rows

                cmdString = "Select BI_ADDR1, BI_ADDR2, BI_CITY, BI_ZIP, BI_SRV_DESC " _
                          & "FROM(CIS28013.BI_SRV_LOC) " _
                          & "WHERE(BI_SRV_LOC_NBR = " & dr("Srv_Loc_Nbr") & ")"
                cmd.CommandText = cmdString
                rdr = cmd.ExecuteReader
                While rdr.Read
                    If rdr.HasRows Then
                        dr("SrvAddr1") = rdr(0).ToString
                        dr("SrvAddr2") = rdr(1).ToString
                        dr("SrvDesc") = rdr(4).ToString
                        dr("City") = rdr(2).ToString
                        dr("Zip") = rdr(3).ToString
                    End If
                End While
                rdr.Close()
            Next

            Dim output As String = String.Empty
            output = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11};{12};{13};{14:c};{15:c};{16:c}"
            ' Dim sw As New StreamWriter("C:\Temp\StateUsage.Txt", True) ' Used to process a complete history
            Dim sw As New StreamWriter(My.Computer.FileSystem.SpecialDirectories.Temp & "\StateUsage.Txt", False) ' Process 1 month
            If ctr = 0 Then
                sw.WriteLine("AGENCY;LOCATION;SERVADD1;SERVADDR2;SERVDESC;CITY;ZIP;ACCOUNT;METER;BILLING PERIOD;CYCLE START;CYCLE END;KWH USAGE;KW DMD;CONSUMPTION CHG ($);Base Rate ($);TOT INV CHG ($)")
            End If
            ctr += 1
            For Each dr In dt.Rows
                sw.WriteLine(String.Format(output, dr("Name"), dr("Srv_Loc_Nbr").ToString, dr("SrvAddr1"), dr("SrvAddr2"), dr("SrvDesc"), dr("City"), dr("Zip"),
                                                   dr("Account").ToString, dr("Meter").ToString, BillCycle, dr("Cycle_Start").ToString, dr("Cycle_End").ToString,
                                                   dr("KWH").ToString, dr("KW").ToString, dr("Consumption_Charge"), dr("Basic_Charge"), dr("Total_Charge")))
            Next
            sw.Flush()
            sw.Close()
            sendMail(My.Computer.FileSystem.SpecialDirectories.Temp & "\StateUsage.Txt", TextBox1.Text)
        End If
        MessageBox.Show("Task Complete" & vbCrLf & "Processed:  " & dt.Rows.Count.ToString)
    End Sub

    Public Sub sendMail(ByVal AttachFile As String, ByVal prd As String)
        ' Public Sub sendMail(ByVal AttachFile As String)

        Dim message As New Net.Mail.MailMessage
        Dim mailMsg As New Net.Mail.SmtpClient
        Dim userName As String = Environment.UserName
        Dim emailAddress As String

        Using pctx = New PrincipalContext(ContextType.Domain)
            emailAddress = GetADUserDetail(pctx, userName)
        End Using

        Dim fromStr As String = emailAddress

        Dim fromAddr As New MailAddress(fromStr)
        Dim toAddr As New MailAddress("mtenergydata@mt.gov")

        message = New MailMessage(fromAddr, toAddr)
        Dim msgContent As String = "Monthly electric usage and charges from Flathead Electric.  See Attached."
        Dim Attch As Attachment = New Attachment(AttachFile)

        With message
            .From = fromAddr
            .DeliveryNotificationOptions = DeliveryNotificationOptions.OnFailure
            .Sender = fromAddr
            .CC.Add(emailAddress)
            .Subject = "Additional Service Utility Invoice Meter Data Request - Flathead Electric Cooperative"
            .Body = msgContent
            .Attachments.Add(Attch)
        End With

        Try
            With mailMsg
                .Host = "LIAM.fecdomain1.local"
                .Port = 25
                .UseDefaultCredentials = True
                .Send(message)
            End With
        Catch ex As Exception
            MessageBox.Show(ex.ToString)
        End Try
        MessageBox.Show("Mail Sent")
        TextBox1.Text = IncrPeriod(TextBox1.Text)
    End Sub


    Private Sub btnClose_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles btnClose.Click
        Me.Close()
    End Sub

    Private Sub Button2_Click(ByVal sender As System.Object, ByVal e As System.EventArgs) Handles Button2.Click
        sendMail(My.Computer.FileSystem.SpecialDirectories.Temp & "\StateUsage.Txt", "")
    End Sub

    Private Function IncrPeriod(prd As String) As String
        Dim ret As String = String.Empty
        Dim tPrd As Int32 = Convert.ToInt32(TextBox1.Text)
        If TextBox1.Text.EndsWith("12") Then
            tPrd += 89
        Else
            tPrd += 1
        End If
        ret = tPrd.ToString
        Return ret
    End Function



End Class

