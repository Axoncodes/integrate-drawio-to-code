class Address {
	public country: Country;
	// public state: State;
	public zip_code: Number;
	public street: Street;
	public digital_addresses: arr(Digital Address);
	public distance_from_user(type): Measure;
}
class Digital_Address3 {
	public provider: Provider;
	public link: String;
	public method(type): type;
}
class Place {
	public address: Address;
	public rate: Rate;
	public schedule: arr(Daily Timetable);
	public status: Status;
	public personnel: arr(Personnel);
	public space_matrix: Space Matrix // find a better name;
	public services: arr(Service);
	public distance_from_user(type): Measure;
}