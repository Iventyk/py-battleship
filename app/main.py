class Deck:
    def __init__(self, row: int, column: int, is_alive: bool = True) -> None:
        self.row = row
        self.column = column
        self.is_alive = is_alive


class Ship:
    def __init__(self, start: tuple, end: tuple) -> None:
        self.start = start
        self.end = end
        self.decks = []
        self.is_drowned = False

        if start[0] == end[0]:  # horizontal ship
            row = start[0]
            for column in range(start[1], end[1] + 1):
                self.decks.append(Deck(row, column))
        else:  # vertical ship
            column = start[1]
            for row in range(start[0], end[0] + 1):
                self.decks.append(Deck(row, column))

    def get_deck(self, row: int, column: int) -> Deck | None:
        for deck in self.decks:
            if deck.row == row and deck.column == column:
                return deck
        return None

    def fire(self, row: int, column: int) -> str:
        deck = self.get_deck(row, column)
        if deck is None:
            return "Miss!"
        deck.is_alive = False
        for deck in self.decks:
            if deck.is_alive:
                return "Hit!"
        self.is_drowned = True
        return "Sunk!"


class Battleship:
    def __init__(self, ships: list) -> None:
        processed_ships = []
        for ship in ships:
            if isinstance(ship, Ship):
                processed_ships.append(ship)
            else:
                processed_ships.append(Ship(ship[0], ship[1]))

        self.ships = processed_ships
        self.field = [["~" for _ in range(10)] for _ in range(10)]
        self.ship_positions = {}

        self.place_ships()

    def place_ships(self) -> None:
        for ship in self.ships:
            for deck in ship.decks:
                self.field[deck.row][deck.column] = "□"
                self.ship_positions[(deck.row, deck.column)] = ship

    def fire(self, location: tuple) -> str:
        row, column = location
        if (row, column) not in self.ship_positions:
            return "Miss!"
        ship = self.ship_positions[(row, column)]
        result = ship.fire(row, column)
        if result == "Hit!":
            self.field[row][column] = "*"
        elif result == "Sunk!":
            for deck in ship.decks:
                self.field[deck.row][deck.column] = "x"
        return result

    def print_field(self) -> None:
        for row in self.field:
            print(" ".join(row))
