<script lang="ts">
	import { Column, Row } from 'carbon-components-svelte';
	import Metric from './dashboard/Metric.svelte';

	export let parcel_data: object;
	export let order_id: object;

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
			<td>Ordered</td>
			<td>{parcel_data && 'time_ordered' in parcel_data ? parcel_data['time_ordered'] : 'None'}</td>
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
