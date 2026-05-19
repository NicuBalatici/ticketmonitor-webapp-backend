DROP TABLE Messages;
DROP TABLE Conversations;
DROP TABLE INCIDENT_TICKETS;
DROP TABLE Users;
DROP TABLE Teams;

--1. Crearea tabelului pentru Echipe
CREATE TABLE Teams
(
    TeamID   INT PRIMARY KEY IDENTITY (1,1),
    TeamName VARCHAR(50) NOT NULL UNIQUE
);

-- 2. Crearea tabelului pentru Utilizatori/Angajați
CREATE TABLE Users
(
    UserID   INT PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL UNIQUE,
    Email    VARCHAR(100),
    Team     VARCHAR(50)  NOT NULL, -- Legatura catre tabela Teams
    FOREIGN KEY (Team) REFERENCES Teams (TeamName)
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
    Team                 VARCHAR(50),  -- Legatura catre tabela Teams
    Assigned_Person      VARCHAR(100), -- Legatura catre tabela Users
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
    FOREIGN KEY (Assigned_Person) REFERENCES Users (FullName),
    FOREIGN KEY (Team) REFERENCES Teams (TeamName)
);

CREATE TABLE Conversations
(
    ConversationID INT PRIMARY KEY IDENTITY (1,1),
    UserID         INT         NOT NULL,
    Ticket         VARCHAR(20) NOT NULL, --De ce ii Ticket_Number varchar si nu int?

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

INSERT INTO Users(UserID, FullName, Email, Team)
VALUES (0, 'John Doe', 'JohnDoe@example.com', 'One')
INSERT
INTO Users(UserID, FullName, Email, Team)
VALUES (1, 'Stan Castan', 'StanCastan@example.com', 'One')

INSERT INTO INCIDENT_TICKETS (Ticket_Number, Status, Priority, Company, Project, Team, Assigned_Person, Service,
                              Description, Notes, Resolution, Cat_T1, Cat_T2, Cat_T3, Resolution_Category,
                              Pending_Duration)
VALUES ('1', 'Open', 'Medium', 'Profi', 'Project', 'One', 'Stan Castan', 'Service', 'Description', 'Notes',
        'Resolution', 'Cat_T1', 'Cat_T2', 'Cat_T3', 'idk', 1)

INSERT INTO Conversations (UserID, Ticket)
VALUES (1, '1')

INSERT INTO Messages (ConversationID, SenderRole, Message)
VALUES (0, 'System', 'You are a helpfull assistan')

