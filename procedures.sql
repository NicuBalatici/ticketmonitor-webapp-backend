DROP PROCEDURE dbo.createConversation
DROP PROCEDURE dbo.getConversation
DROP PROCEDURE dbo.getMessageHistory
DROP PROCEDURE dbo.insertUserMessage
DROP PROCEDURE dbo.insertAssistantMessage
GO

-- Creates new conversation and returns its ID
CREATE PROCEDURE dbo.createConversation
    @UserID INT = 0,
    @TicketID nvarchar(MAX) = NULL
AS
    SET NOCOUNT ON;
    INSERT INTO Conversations(UserID, Ticket)
    VALUES (@UserID, @TicketID);
    SELECT ConversationID FROM Conversations WHERE UserID = @UserID AND Ticket = @TicketID;
GO


CREATE PROCEDURE dbo.getConversation
    @ConversationID INT = 0
AS
    SET NOCOUNT ON;
    SELECT ConversationID FROM Conversations WHERE ConversationID = @ConversationID;
GO


CREATE PROCEDURE dbo.getMessageHistory
    @ConversationID INT = 0
AS
    SET NOCOUNT ON;
    SELECT SenderRole, Message, Sent_Datetime FROM Messages
    WHERE ConversationID = @ConversationID
    ORDER BY Sent_Datetime
GO


CREATE PROCEDURE dbo.insertUserMessage
    @ConversationID INT = 0,
    @Message nvarchar(MAX) = NULL
AS
    SET NOCOUNT ON;
    INSERT INTO Messages(ConversationID, SenderRole, Message, Sent_Datetime)
    VALUES (@ConversationID, 'User', @Message, GETDATE());
GO


CREATE PROCEDURE dbo.insertAssistantMessage
    @ConversationID INT = 0,
    @Message nvarchar(MAX) = NULL
AS
    SET NOCOUNT ON;
    INSERT INTO Messages(ConversationID, SenderRole, Message, Sent_Datetime)
    VALUES (@ConversationID, 'Assistant', @Message, GETDATE());
GO

EXECUTE createConversation 1, 1