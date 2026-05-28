DROP TABLE Messages;
DROP TABLE Conversations;
DROP TABLE INCIDENT_TICKETS;
DROP TABLE Users;
DROP TABLE Teams;

--1. Crearea tabelului pentru Echipe
CREATE TABLE Teams
(
    TeamID   INT PRIMARY KEY IDENTITY (1,1),
    TeamName VARCHAR(50) NOT NULL
);

-- 2. Crearea tabelului pentru Utilizatori/Angajați
CREATE TABLE Users
(
    UserID   INT PRIMARY KEY IDENTITY (1,1),
    FullName VARCHAR(100) NOT NULL,
    Email    VARCHAR(100),
    Team     INT  NOT NULL, -- Legatura catre tabela Teams
    FOREIGN KEY (Team) REFERENCES Teams (TeamID)
);

-- 3. Crearea tabelului principal de Tickete
CREATE TABLE INCIDENT_TICKETS
(
    Ticket_Number        VARCHAR(20) PRIMARY KEY,

    Status               VARCHAR(30)
        CHECK (Status IN ('Open', 'In Progress', 'Resolved', 'Closed', 'Waiting for Customer')),

    Priority             VARCHAR(10)
        CHECK (Priority IN ('High', 'Medium', 'Low', 'Critical')),

    Company              VARCHAR(100),
    Project              VARCHAR(100),
    Team                 INT, -- Legatura catre tabela Teams
    Assigned_Person      INT, -- Legatura catre tabela Users
    Service              VARCHAR(100),
    Description          TEXT,
    Notes                TEXT,
    Resolution           TEXT,

    Cat_T1               VARCHAR(50),
    Cat_T2               VARCHAR(50),
    Cat_T3               VARCHAR(50),

    Submit_Datetime      DATETIME DEFAULT GETDATE(),
    Resolved_Datetime    DATETIME NULL,
    Closed_Datetime      DATETIME NULL,
    Last_Modified        DATETIME DEFAULT GETDATE(),
    Estimated_Resolution DATETIME NULL,

    Resolution_Category  VARCHAR(50),
    Pending_Duration     INT,

    -- Chei externe
    FOREIGN KEY (Assigned_Person) REFERENCES Users (UserID),
    FOREIGN KEY (Team) REFERENCES Teams (TeamID)
);

CREATE TABLE Conversations
(
    ConversationID INT PRIMARY KEY IDENTITY (1,1),
    UserID         INT         NOT NULL,
    Ticket         VARCHAR(20) NOT NULL,

    FOREIGN KEY (UserID) REFERENCES Users (UserID),
    FOREIGN KEY (Ticket) REFERENCES INCIDENT_TICKETS (Ticket_Number)
);

CREATE TABLE Messages
(
    MessageID      INT PRIMARY KEY IDENTITY (1,1),
    ConversationID INT          NOT NULL,
    SenderRole     VARCHAR(20)  NOT NULL
        CHECK (SenderRole IN ('System', 'Assistant', 'User', 'Developer', 'CompletionTool', 'Function')),
    Message        VARCHAR(MAX) NOT NULL,
    Sent_Datetime  DATETIME DEFAULT GETDATE(),

    FOREIGN KEY (ConversationID) REFERENCES Conversations (ConversationID),
);

INSERT INTO Teams(TeamName)
VALUES ('One');
INSERT INTO Teams(TeamName)
VALUES ('Two');
INSERT INTO Teams(TeamName)
VALUES ('Three');

INSERT INTO Users(FullName, Email, Team)
VALUES ('Stan Castan', 'StanCastan@example.com', 1)
INSERT INTO Users(FullName, Email, Team)
VALUES ('Hector Vector', 'HectorVector@example.com', 1)

INSERT INTO Users(FullName, Email, Team)
VALUES ('Spiderman', 'Spiderman@example.com', 2)
INSERT INTO Users(FullName, Email, Team)
VALUES ('Spongebob', 'Spongebob@example.com', 2)

INSERT INTO Users(FullName, Email, Team)
VALUES ('Nicola Tesla', 'NicolaTesla@example.com', 3)
INSERT INTO Users(FullName, Email, Team)
VALUES ('Erwin Schrodinger', 'ErwinSchrodinger@example.com', 3)

-- INSERT INTO Conversations (UserID, Ticket)
-- VALUES (1, '1')

-- INSERT INTO Messages (ConversationID, SenderRole, Message)
-- VALUES (1, 'System', 'You are a helpfull assistan')

