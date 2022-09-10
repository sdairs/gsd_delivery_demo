<script lang="ts">
	import {} from 'carbon-components-svelte';

	export let parcel_data: object;
</script>

<table class="order-table">
	<tbody>
		<tr>
			<td>Order ID</td>
			<td>{parcel_data['order_id']}</td>
		</tr>
		<tr>
			<td>Driver ID</td>
			<td>{parcel_data['driver_id']}</td>
		</tr>
		<tr>
			<td>Ordered</td>
			<td>{parcel_data['time_ordered']}</td>
		</tr>
		<tr>
			<td>Collected</td>
			<td>{parcel_data['time_collected']}</td>
		</tr>
		<tr>
			<td>At Depot</td>
			<td>{parcel_data['time_at_depot']}</td>
		</tr>
		<tr>
			<td>With driver</td>
			<td>{parcel_data['time_with_driver']}</td>
		</tr>
		<tr>
			<td>Delivered</td>
			<td>{parcel_data['time_delivered']}</td>
		</tr>
	</tbody>
</table>

<style>
	.order-table {
		border-collapse: collapse;
		margin: 25px 0;
		font-size: 0.9em;
		font-family: sans-serif;
		min-width: 400px;
		box-shadow: 0 0 20px rgba(0, 0, 0, 0.15);
	}
	.order-table thead tr {
		background-color: #009879;
		color: #ffffff;
		text-align: left;
	}
	.order-table th,
	.order-table td {
		padding: 12px 15px;
	}
	.order-table tbody tr {
		border-bottom: 1px solid #383838;
	}

	.order-table tbody tr:nth-of-type(even) {
		background-color: #252525;
	}

	.order-table tbody tr:last-of-type {
		border-bottom: 2px solid #009879;
	}
</style>
