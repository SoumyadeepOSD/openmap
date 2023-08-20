import phonenumbers
from phonenumbers import geocoder, carrier, timezone

x = phonenumbers.parse("+917667244137", None)
country = geocoder.description_for_number(x, "en")
carrier = carrier.name_for_number(x, "en")
timezone = timezone.time_zones_for_number(x)
print(country)
print(carrier)
print(timezone)

