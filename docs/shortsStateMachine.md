```Mermaid

flowchart TB
    Machine{STATE MACHINE}-->Root
    Root{ROOT_STATE}-->Search(Searching for note)
    Reset((RESET THE BOT!!!))-->Root

    subgraph Find note
        Search-->|Note detected|Move(Move to note)
        Move-->|Note lost|Search
        Move-->Lineup(Lineup to intake note)
        Lineup-->|Note lost|Search
    end
 
    subgraph Intaking Note
        Lineup-->Spin(Spin intake motors)
        Spin-->|Check for note|Spin
        Spin & Gloop-->|Note lost|Reset
        Spin-->|Note intaken|Change(Clamp note)
        Change-->|Fatal error or something|Reverse(Reverse Motors)
        Reverse-->Reset
        Change-->Gloop(Take Augstus Gloop up the tube)
        Gloop-->|Check note position|Gloop
    end

    subgraph Fire Note
        Gloop-->ReadyFire(Prepare for fire)
        ReadyFire-->|Check disk|ReadyFire
        ReadyFire--->Fire(FIRE!)
        Fire-->Reset
    end
```