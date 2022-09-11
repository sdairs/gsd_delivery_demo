<script lang="ts">
	export let parcel_data: object;
	export let order_id: string;
	export let order_time: string;
	let driver_name: string;

	async function get_driver_name(driver_id: string) {
		let params: URLSearchParams = new URLSearchParams({ driver_id: driver_id });
		let url = new URL('https://api.tinybird.co/v0/pipes/get_driver_name_by_id.json?' + params);

		const result = await fetch(url, {
			headers: {
				Authorization:
					'Bearer p.eyJ1IjogImQwZWIyNzhmLTk4ZTQtNDMxNC1hMDMzLWM0OTBkZDU1ODQ0MCIsICJpZCI6ICJiYmYwOTAzMy03ODAzLTQ4M2YtODNmMi1iOGQ5N2Q0NzBiNDMifQ.kdShMAz3fwT2jrge3ZDYN3ft02qKlipUpt2_nqrpWFI'
			}
		}).then((r) => r.json());

		driver_name = result['data'][0]['name'];
	}

	$: {
		parcel_data;
		if (
			'driver_id' in parcel_data &&
			(parcel_data['driver_id'] != '' || parcel_data['driver_id'] != undefined)
		) {
			get_driver_name(parcel_data['driver_id']);
		}
	}
</script>

<table class="tracker-table">
	<tbody>
		<tr>
			<td>Order ID</td>
			<td>{order_id}</td>
		</tr>
		<tr>
			<td>Driver ID</td>
			<td>{parcel_data && 'driver_id' in parcel_data ? parcel_data['driver_id'] : 'None'}</td>
		</tr>
		<tr>
			<td>Driver Name</td>
			<td>{driver_name ? driver_name : 'None'}</td>
		</tr>
		<tr>
			<td>Ordered</td>
			<td>{order_time}</td>
		</tr>
		<tr>
			<td>Collected</td>
			<td
				>{parcel_data && 'time_collected' in parcel_data
					? parcel_data['time_collected']
					: 'None'}</td
			>
		</tr>
		<tr>
			<td>At Depot</td>
			<td
				>{parcel_data && 'time_at_depot' in parcel_data ? parcel_data['time_at_depot'] : 'None'}</td
			>
		</tr>
		<tr>
			<td>With driver</td>
			<td
				>{parcel_data && 'time_with_driver' in parcel_data
					? parcel_data['time_with_driver']
					: 'None'}</td
			>
		</tr>
		<tr>
			<td>Delivered</td>
			<td
				>{parcel_data && 'time_delivered' in parcel_data
					? parcel_data['time_delivered']
					: 'None'}</td
			>
		</tr>
	</tbody>
</table>

<style>
	.tracker-table {
		border-collapse: collapse;
		width: 100%;
		font-size: 0.9em;
		font-family: sans-serif;
		box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
	}
	.tracker-table thead tr {
		background-color: #009879;
		color: #ffffff;
		text-align: left;
	}
	.tracker-table th,
	.tracker-table td {
		padding: 12px 15px;
	}
	.tracker-table tbody tr {
		border-bottom: 1px solid #383838;
	}

	.tracker-table tbody tr:nth-of-type(even) {
		background-color: #252525;
	}

	.tracker-table tbody tr:last-of-type {
		border-bottom: 2px solid #009879;
	}
</style>
