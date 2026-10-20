class BookingPolicy:
    def validate_booking(self, duration, hour):
        return True


class JohannesburgPolicy(BookingPolicy):

    def validate_booking(self, duration, hour):
        return duration <= 3


class PretoriaPolicy(BookingPolicy):

    def validate_booking(self, duration, hour):
        return 8 <= hour <= 17


class DurbanPolicy(BookingPolicy):

    def validate_booking(self, duration, hour):
        return duration <= 2 and 9 <= hour <= 16


campus_policies = {
    "Johannesburg": JohannesburgPolicy(),
    "Pretoria": PretoriaPolicy(),
    "Durban": DurbanPolicy()
}
